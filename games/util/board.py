# base example from: https://pythonspot.com/game-development-with-pygame/

#! /usr/bin/env python3
# encoding: utf-8

import random
import pygame
from pygame.locals import *

# https://en.wikipedia.org/wiki/X11_color_names (not all apply)
COLORS1 = [
    'RED',
    'GREEN',
    'BLUE',
    'YELLOW',
    'ORANGE',
    'PURPLE',
    'FOREST GREEN',
    'PINK',
]

COLORS2 = [
    'Goldenrod',
    'Khaki',
    'Olive Drab',
    'Yellow Green',
    'Brown',
    'Chocolate',
    'Dark Magenta',
    'Dark Gray',
]

LEFT = 1
RIGHT = 2
TOP = 3
BOTTOM = 4

# Game state constants
START = 1
RUN = 2
END = 3

# Draw type constants
CIRCLE = 0 # default
RECTANGLE = 1

class Board:
    def __init__(self, drawPos = [0, 0], drawSize = [400, 400], drawType = CIRCLE):
        # Tile parameters
        default = 20
        self.countX = default
        self.countY = default
        self.sizeX = default
        self.sizeY = default

        # Board parameters
        self.drawRect = Rect(drawPos, drawSize)
        self.autoPosition = True
        self.boardRect = Rect(0, 0, 0, 0)

        self.players = 4
        self.colors = COLORS2
        if self.players > len(self.colors):
            self.players = len(self.colors)
        self.warpVertical = False # How to draw warpping?? white triangles pointin out??
        self.warpHorizonal = False
        # If warpping selected, draw offset Rect with the same tiles?
        self.adjacenFunction = self.getAdjacent4
        # self.adjacenFunction = self.getAdjacent6 # 6 sided tiles NOT IMPLEMENTED
        # self.adjacenFunction = self.getAdjacent8

        if drawType == RECTANGLE:
            self.drawFunction = self.drawTileRect
        else:
            self.drawFunction = self.drawTileCircle

        self.board = [0] * (self.countX * self.countY)
        self.movesCount = 0
        self.gameState = START

        self.selected = None
        self.adjacent = []
        self.active = False
        self.setBoardDrawArea()
        self.populateBoard() # Demo mode???
        # Allow blanks??

    def populateBoard(self, noBlanks = 1):
        for tile in range(0, len(self.board)):
            self.board[tile] = random.randint(noBlanks, self.players)

    def initBoard(self, tileSize = None, tileCount = None, players = None, colorPalette = None):
        if tileSize:
            if 'index' in dir(tileSize) and len(tileSize) > 1:
                self.sizeX = tileSize[0]
                self.sizeY = tileSize[1]
            else:
                self.sizeX = tileSize
                self.sizeY = tileSize

        if tileCount:
            if 'index' in dir(tileCount) and len(tileCount) > 1:
                self.countX = tileCount[0]
                self.countY = tileCount[1]
            else:
                self.countX = tileCount
                self.countY = tileCount

        if players:
            if players > 1:
                self.players = players
            else:
                self.players = 2
        if colorPalette:
            self.colors = colorPalette

        if self.players > len(self.colors):
            self.players = len(self.colors)

        self.board = [0] * (self.countX * self.countY)
        self.movesCount = 0
        self.selected = None
        self.adjacent = []

        self.setBoardDrawArea()
        self.populateBoard()
        self.gameState = RUN
        return True

    def setBoardDrawArea(self, drawPos = None, drawSize = None, boardOffset = None, moveBoard = None):
        if drawPos: self.drawRect.move_ip(drawPos)
        if drawSize: self.drawRect.size =  drawSize
        self.boardRect.size = [self.countX * self.sizeX, self.countY * self.sizeY]
        if boardOffset:
            self.boardRect.topleft = boardOffset # set absolute offset
            self.autoSize = False
        elif moveBoard:
            self.boardRect.move_ip(moveBoard) # move relative offset
            self.autoSize = False
        elif self.autoPosition:
            self.boardRect.centerx = self.drawRect.centerx
            self.boardRect.centery = self.drawRect.centery
            # print (self.boardRect, self.drawRect)

    def drawTileCircle(self, surface, tile, color = None):
        if self.board[tile]:
            tileCenterX = self.boardRect.x + tile % self.countX * self.sizeX + int(self.sizeX / 2)
            tileCenterY = self.boardRect.y + int(tile / self.countX) * self.sizeY + int(self.sizeY / 2)
            if tileCenterX > -self.sizeX and tileCenterX < self.drawRect.right + self.sizeX and \
                    tileCenterY > -self.sizeY and tileCenterY < self.drawRect.bottom + self.sizeY:
                # Draw only if inside draw area
                if color:
                    size = int(self.sizeX / 4)
                else:
                    color = pygame.color.Color(self.colors[self.board[tile] - 1])
                    size = int(self.sizeX / 2)

                pygame.draw.circle(surface, color, (tileCenterX, tileCenterY), size, 0)

    def drawTileRect(self, surface, tile, color = None):
        tileRect = Rect(self.boardRect.x + tile % self.countX * self.sizeX,
            self.boardRect.y + int(tile / self.countX) * self.sizeY,
            self.sizeX, self.sizeY)
        if tileRect.colliderect(self.drawRect):
            # Draw only if inside draw area
            if color:
                tileRect.inflate_ip(-self.sizeX / 2, -self.sizeY / 2)
            else:
                color = pygame.color.Color(self.colors[self.board[tile] - 1])

            pygame.draw.rect(surface, color, tileRect, 0)

    def draw(self, surface, image = None):
        surface.fill([0,0,32])
        # pygame.draw.rect(surface, [255,255,255], self.boardRect, 2)
        # pygame.draw.rect(surface, [0,255,0], self.drawRect, 2)
        firstTileToDraw = int((self.drawRect.top - self.boardRect.top) / self.sizeY) * self.countX
        lastTileToDraw = int((self.drawRect.bottom - self.boardRect.bottom + self.boardRect.height + self.sizeY) / self.sizeY) * self.countX
        # print (firstTileToDraw, lastTileToDraw)
        for i in range(0, len(self.board)):
            if i >= firstTileToDraw and i < lastTileToDraw:
                self.drawFunction(surface, i)

        if self.selected != None:
            self.drawTileCircle(surface, self.selected, [0,0,0])
            # self.drawFunction(surface, self.selected, [0,0,0])

        for i in self.adjacent:
            self.drawTileCircle(surface, i, [255,255,255])
            # self.drawFunction(surface, i, [255,255,255])

    def on_loop(self):
        self.determineGameEnd()

    def on_event(self, event):
        if self.active and event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.boardRect.collidepoint(x, y):
                tile = int((x - self.boardRect.x) / self.sizeX) + \
                        int((y - self.boardRect.y) / self.sizeY) * self.countX
                # print (x, y, int(x / self.sizeX), int(y / self.sizeX), tile)
                if self.selected == tile:
                    self.selected = None
                    self.adjacent = []
                elif tile in self.adjacent:
                    if self.fillArea(tile, self.board[self.selected]):
                        self.movesCount += 1
                    self.selected = None
                    self.adjacent = []
                else:
                    self.selected = tile
                    self.adjacent = self.adjacenFunction(tile)

    def getAdjacent4(self, tile):
        adjacents = []
        if not self.isOnEdge(tile, LEFT):
            adjacents.append(tile - 1)
        elif self.warpVertical:
            adjacents.append(tile - 1 + self.countX)

        if not self.isOnEdge(tile, RIGHT):
            adjacents.append(tile + 1)
        elif self.warpVertical:
            adjacents.append(tile + 1 - self.countX)

        if not self.isOnEdge(tile, TOP):
            adjacents.append(tile - self.countX)
        elif self.warpHorizonal:
            adjacents.append(tile + len(self.board) - self.countX)

        if not self.isOnEdge(tile, BOTTOM):
            adjacents.append(tile + self.countX)
        elif self.warpHorizonal:
            adjacents.append(tile - len(self.board) + self.countX)

        return adjacents

    def getAdjacent8(self, tile):
        adjacents = []
        if not self.isOnEdge(tile, LEFT):
            adjacents.append(tile - 1)

            if not self.isOnEdge(tile, TOP):
                adjacents.append(tile - 1 - self.countX)
                # print ('nL nT', tile - 1 - self.countX)
            elif self.warpHorizonal:
                adjacents.append(tile - 1 + len(self.board) - self.countX)
                # print ('nL T', tile - 1 + len(self.board) - self.countX)

            if not self.isOnEdge(tile, BOTTOM):
                adjacents.append(tile - 1 + self.countX)
                # print ('nL nB', tile - 1 + self.countX)
            elif self.warpHorizonal:
                adjacents.append(tile - 1 - len(self.board) + self.countX)
                # print ('nL B', tile - 1 - len(self.board) + self.countX)

        elif self.warpVertical:
            adjacents.append(tile - 1 + self.countX)

            if not self.isOnEdge(tile, TOP):
                adjacents.append(tile - 1)
                # print ('L nT', tile - 1)
            elif self.warpHorizonal:
                adjacents.append(tile - 1 + len(self.board))
                # print ('L T', tile - 1 + len(self.board))

            if not self.isOnEdge(tile, BOTTOM):
                adjacents.append(tile - 1 + self.countX * 2)
                # print ('L nB', tile - 1 + self.countX * 2)
            elif self.warpHorizonal:
                adjacents.append(tile - 1 - len(self.board) + self.countX * 2)
                # print ('L B', tile - 1 - len(self.board) + self.countX * 2)

        if not self.isOnEdge(tile, RIGHT):
            adjacents.append(tile + 1)

            if not self.isOnEdge(tile, TOP):
                adjacents.append(tile + 1 - self.countX)
                # print ('nR nT', tile + 1 - self.countX)
            elif self.warpHorizonal:
                adjacents.append(tile + 1 + len(self.board) - self.countX)
                # print ('nR T', tile + 1 + len(self.board) - self.countX)

            if not self.isOnEdge(tile, BOTTOM):
                adjacents.append(tile + 1 + self.countX)
                # print ('nR nB', tile + 1 + self.countX)
            elif self.warpHorizonal:
                adjacents.append(tile + 1 - len(self.board) + self.countX)
                # print ('nR B', tile + 1 - len(self.board) + self.countX)

        elif self.warpVertical:
            adjacents.append(tile + 1 - self.countX)

            if not self.isOnEdge(tile, TOP):
                adjacents.append(tile + 1 - self.countX * 2)
                # print ('R nT', tile + 1 - self.countX * 2)
            elif self.warpHorizonal:
                adjacents.append(tile + 1 + len(self.board) - self.countX * 2 )
                # print ('R T', tile + 1 + len(self.board) - self.countX * 2 )

            if not self.isOnEdge(tile, BOTTOM):
                adjacents.append(tile + 1)
                # print ('R nB', tile + 1)
            elif self.warpHorizonal:
                adjacents.append(tile + 1 - len(self.board))
                # print ('R B', tile + 1 - len(self.board))

        if not self.isOnEdge(tile, TOP):
            adjacents.append(tile - self.countX)
        elif self.warpHorizonal:
            adjacents.append(tile + len(self.board) - self.countX)

        if not self.isOnEdge(tile, BOTTOM):
            adjacents.append(tile + self.countX)
        elif self.warpHorizonal:
            adjacents.append(tile - len(self.board) + self.countX)

        return adjacents

    def isOnEdge(self, tile, direction):
        if direction == LEFT:
            return tile % self.countX == 0
        elif direction == RIGHT:
            return tile % self.countX == self.countX -1
        elif direction == TOP:
            return tile < self.countX
        elif direction == BOTTOM:
            return tile >= len(self.board) - self.countX

    def getArea(self, area):
        areaPlayer = self.board[area]
        areaTiles = set([area])
        adjacents = self.adjacenFunction(area)
        while adjacents:
            t = adjacents.pop()
            if self.board[t] == areaPlayer and not t in areaTiles:
                areaTiles.add(t)
                adjacents += self.adjacenFunction(t)
        return areaTiles

    def fillArea(self, area, player):
        areaPlayer = self.board[area]
        if areaPlayer != player:
            tiles = self.getArea(area)
            for t in tiles:
                self.setBoardTile(t, player)
            return True
        return False

    def setBoardTile(self, tile, player):
        self.board[tile] = player

    def getMovesCount(self):
        return self.movesCount

    def getGameState(self):
        return self.gameState

    def determineGameEnd(self):
        if len(set(self.board)) <= 1:
            self.gameState = END

    def setPassive(self):
        self.active = False

    def setActive(self):
        self.active = True

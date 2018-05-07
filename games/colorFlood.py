#! /usr/bin/env python3
# encoding: utf-8

import random
import pygame
from pygame.locals import *
import time

import sys, os
sys.path.append(os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ))

from data.textToScreen import textToScreen
from data.gameMenu import MenuContainer, MenuItem
from data.highScore import HighScore
from games.util.board import Board

# Game state constants
START = 1
RUN = 2
END = 3

SIZELIST = [10, 20, 40]

class Game:
    windowPos = (0, 0)
    windowSize = (600, 800)
    name = 'colorFlood'

    def __init__(self, players = 4):
        # Game values
        self._running = True
        self.gameStartTime = 0
        self.gameduration = '0:00'
        self.gameState = START

        # Hiscore
        self.hiscore = HighScore(self.name)

        # Board parameters
        self.boardOffset = [0, 0]
        self.boardSize = [600, 600]
        self.board = Board(self.boardOffset, self.boardSize)
        self.tileCountIterator = 0
        self.players = players
        self.maxPlayers = 8

        # Start menu
        self.startMenu = MenuContainer(Rect(100,100,400,400), textPadding = (20, 20))
        self.startMenu.addItem(MenuItem('ColorFlood'))
        self.startMenu.addItem(MenuItem('Players', textFormat = "{1} {0}",
            textSize = 30, padding = 30, value = 0,
            uFunc = self.menuGetPlayers, cFunc = self.menuSetPlayers))
        self.startMenu.addItem(MenuItem('Board size', textFormat = "{0} {1}x{1}",
            textSize = 30, padding = 10, value = 0,
            uFunc = self.menuGetBoardSize, cFunc = self.menuSetBoardSize))
        self.startMenu.addItem(MenuItem('Start', padding = 30, cFunc = self.startGame))
        self.startMenu.addItem(MenuItem('Exit', padding = 70, cFunc = self.exitGame))

        # Game menu parameters
        self.gameMenu = MenuContainer(Rect(600,0,200,600))
        self.gameMenu.addItem(MenuItem('Time', padding = 20))
        self.gameMenu.addItem(MenuItem('', textSize = 30, textFormat = "{:>6}", uFunc = self.menuGetTime))
        self.gameMenu.addItem(MenuItem('Moves', padding = 20))
        self.gameMenu.addItem(MenuItem('', textSize = 30, textFormat = "{:>5}", uFunc = self.menuGetMoves))
        self.gameMenu.addItem(MenuItem('End game', textSize = 30, padding = 300, cFunc = self.endGame))
        self.gameMenu.setActive()

        # End menu
        self.endMenu = MenuContainer(Rect(100,100,400,400), textPadding = (20, 20))
        self.endMenu.addItem(MenuItem('Game ended'))
        self.endMenu.addItem(MenuItem('moves', textFormat = "{1} {0}", value = 0, padding = 20, uFunc = self.board.getMovesCount, textSize = 30))
        self.endMenu.addItem(MenuItem('Time', textFormat = "{0} {1}", value = 0, padding = 20, uFunc = self.menuGetTime, textSize = 30))
        self.endMenu.addItem(MenuItem('Continue', padding = 20, cFunc = self.initGame))
        # print (self.startMenu, self.endMenu)

        self.initGame()

    def initGame(self):
        self.gameState = START
        self.startMenu.setActive()
        self.endMenu.setPassive()
        self.board.setPassive()

    def startGame(self):
        if self.board.initBoard(tileCount = SIZELIST[self.tileCountIterator], players = self.players):
            # print ('start game')
            self.gameStartTime = pygame.time.get_ticks()
            self.gameduration = '0:00'
            self.gameState = RUN
            self.startMenu.setPassive()
            self.endMenu.setPassive()
            self.board.setActive()

    def endGame(self):
        if self.gameState == RUN:
            self.gameduration = pygame.time.get_ticks() - self.gameStartTime
            self.gameduration = "{:d}:{:02d}".format(
                int((self.gameduration / 1000) / 60), int(self.gameduration / 1000) % 60)
            # print ('Game ended with {0} moves at time {1}'.format(self.board.getMovesCount(), self.gameduration))
            if self.board.getGameState() == END: # Only if board complete
                self.hiscore.addScore(self.generateLevelString(),
                    time.strftime("%y-%m-%d_%H:%M:%S", time.gmtime()),
                    self.board.getMovesCount(),
                    self.gameduration)
                self.hiscore.save()
                self.hiscore.printScores(self.generateLevelString())
            self.gameState = END
            self.startMenu.setPassive()
            self.endMenu.setActive()
            self.board.setPassive()

    def exitGame(self):
        self.hiscore.save()
        self._running = False
        # print ("exit")

    def draw(self, surface, image = None):
        self.board.draw(surface)
        self.gameMenu.draw(surface)
        self.startMenu.draw(surface)
        self.endMenu.draw(surface)

    def gameLoop(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        if (keys[K_ESCAPE]):
            self._running = False

        if (keys[K_RIGHT] or keys[K_d]):
            self.board.setBoardDrawArea(moveBoard = (20, 0))

        if (keys[K_LEFT] or keys[K_a]):
            self.board.setBoardDrawArea(moveBoard = (-20, 0))

        if (keys[K_UP] or keys[K_w]):
            self.board.setBoardDrawArea(moveBoard = (0, -20))

        if (keys[K_DOWN] or keys[K_s]):
            self.board.setBoardDrawArea(moveBoard = (0, 20))

        if (keys[K_q]):
            self.board.setBoardDrawArea(boardOffset = (0, 0))

        if self.gameState == RUN:
            self.board.on_loop()

        self.gameMenu.update()
        self.startMenu.update()
        self.endMenu.update()

        if self.gameState == RUN and self.board.getGameState() == END:
            self.endGame()

    def gameEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.board.on_event(event)
            self.gameMenu.onMouseClick()
            self.startMenu.onMouseClick()
            self.endMenu.onMouseClick()

    def generateLevelString(self):
        return '{0}x{0}p{1}'.format(SIZELIST[self.tileCountIterator], self.players)

    def menuGetTime(self):
        if self.gameState == RUN:
            time = pygame.time.get_ticks() - self.gameStartTime
            return "{:d}:{:02d}".format(
                int((time / 1000) / 60), int(time / 1000) % 60)
        else:
            return self.gameduration

    def menuSetPlayers(self):
        if self.players < self.maxPlayers:
            self.players += 1
        else:
            self.players = 2

    def menuSetBoardSize(self):
        if self.tileCountIterator < len(SIZELIST) - 1:
            self.tileCountIterator += 1
        else:
            self.tileCountIterator = 0

    def menuGetMoves(self):
        return "{:03d}".format(self.board.getMovesCount())

    def menuGetPlayers(self):
        return self.players

    def menuGetBoardSize(self):
        return SIZELIST[self.tileCountIterator]

    def getRunningState(self):
        return self._running

if __name__ == "__main__" :
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    game = Game()
    running = True
    try:
        while( running and game.getRunningState() ):
            for event in pygame.event.get():
                game.gameEvent(event)

            game.gameLoop()
            game.draw(screen)
            pygame.display.flip()
            clock.tick(25)

    except KeyboardInterrupt:
        running = False
    pygame.quit()

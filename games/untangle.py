#!/usr/bin/env python3

import pygame
import random

import math

import sys, os

#print (os.path.abspath(__file__))
#print (os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ))
sys.path.append(os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ))
# https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py

# import util.intersectingLineDetection as det
import util.intersectingSegmentDetection as det

from data.textToScreen import textToScreen

#print (dir(util.intersectingLineDetection))
#print (dir(det))

# https://en.wikipedia.org/wiki/X11_color_names (not all apply)
# pygame.color.Color('Black')

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

class Game:
    name = 'entangled'

    def __init__(self):
        self.rectsAmmount = 20


        self.blockSize = 14
        self.gridSize = self.blockSize /2 +1

        self.colorPalette = {
            'intersecting' : pygame.color.Color('Brown'),
            'nonintersecting' : pygame.color.Color('Lime Green'),
            'selected' : pygame.color.Color('White'),
            'selectedConnecting' : pygame.color.Color('Blue'),
            'marked' : pygame.color.Color('Blue'),
            'markedConnecting' : pygame.color.Color('White'),
            'background' : pygame.color.Color('Dim Gray'),
            'line' : pygame.color.Color('Black'),
        }

        self.selected = None
        self.mark = None
        self.tileMoved = True

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.selfSolveCountdown = 0
        self.selfSolveOrder = []
        self.selfSolveIndex = 0

        self.placeCount = 0
        self.placeNodes = 3
        self.countdown = 25

        # Create nodes (rects)
        self.rects = []
        for x in range(self.rectsAmmount):
            self.rects.append( [pygame.Rect(self.myRound(20),#random.randint(0, SCREEN_WIDTH - self.blockSize), 
                        self.myRound(20),#random.randint(0, SCREEN_HEIGHT - self.blockSize), 
                        self.blockSize, self.blockSize),
                        [], [], self.colorPalette['intersecting']
            ])

        for x in range(len(self.rects)):
            self.selfSolveOrder.append(x)
        random.shuffle(self.selfSolveOrder)

    def getRunningState(self):
        return self.is_running

    def drawCirclePoints(self, points, radius, center = (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))):
        '''
        An algorithm to create positions to points in circle raduis
        Python implementation of:
        https://stackoverflow.com/questions/5300938/calculating-the-position-of-points-in-a-circle
        '''
        positions = []

        slice = 2 * math.pi / points
        for i in range(0, points):
            angle = slice * i
            x = self.myRound(int(center[0] + radius * math.cos(angle)))
            y = self.myRound(int(center[1] + radius * math.sin(angle)))
            positions.append((x,y))
        return positions

    def myRound(self, x):
        '''
        https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
        '''
        return int(self.gridSize * round(float(x)/self.gridSize))

    def testSegmentIntercet(self, i, c):
        collides = False
        for j in range(0, len(self.rects)): # other nodes...
            for d in self.rects[j][1] + self.rects[j][2]: #... ande their connections
                #print (i, c, j, d)
                if j == i or j == c or d == i or d == c: # but not the node or its connections itself
                    pass
                elif det.doIntersect(self.rects[i][0], self.rects[c][0], self.rects[j][0], self.rects[d][0]):
                    return True
                    #print ("collides")
                    break
            if collides:
                break
        return False

    def createRandomConnections(self):
        # Create random connections between nodes
        for i, r in enumerate(self.rects):
            connections = 2
            while connections:
                connection = random.randint(0, len(self.rects)-1)
                if connection != i and not i in self.rects[connection][1]:
                    r[1].append(connection)
                    self.rects[connection][2].append(i)
                    connections -= 1

    def placeOnCircle(self):
        # Create node positions to circle and apply
        circlePositions = self.drawCirclePoints(len(self.rects), 
                    min(len(self.rects)*5, int(SCREEN_WIDTH/2) - self.blockSize , 
                    int(SCREEN_HEIGHT/2) - self.blockSize))
        random.shuffle(circlePositions)
        for i, p in enumerate(circlePositions):
            self.rects[i][0].center = p

    def buildNodesAnimation(self, rects):
        if self.placeNodes == 3:
            groupMembers = 7
            #for i in range(0, int(len(rects)/groupMembers)):
            #    for j in range(0, groupMembers):
            i = int(self.placeCount/groupMembers)
            j = int(self.placeCount%groupMembers)
            #print (i, j)
            currNode = i*groupMembers+j
            if j == 0 and i > 0:
                rects[currNode][1].append(currNode-groupMembers)
                rects[currNode-groupMembers][2].append(currNode)
            if j > 0:
                rects[currNode][1].append(currNode-1)
                rects[currNode-1][2].append(currNode)
            if j > 1:
                rects[currNode][1].append(currNode-2)
                rects[currNode-2][2].append(currNode)
            if j == groupMembers-1 and i > 0:
                rects[currNode][1].append(currNode-groupMembers)
                rects[currNode-groupMembers][2].append(currNode)

            rects[currNode][0].center = (40 + i*80 + self.placeCount%2*20 + random.randint(-10,10),
                    40 + j*40 + random.randint(-10,10))
            self.placeCount += 1
            if self.placeCount >= len(rects):
                self.placeNodes = 2
                if j != 0:
                    tries = groupMembers*3
                    connections = 2
                    while connections and tries:
                        connection = random.randint(max(0, currNode - int(groupMembers*1.5)), currNode-2)
                        if connection != currNode and not connection in rects[currNode][1] and \
                                not self.testSegmentIntercet(currNode, connection):
                            rects[currNode][1].append(connection)
                            rects[connection][2].append(currNode)
                            connections -= 1
                        tries -= 1
                        # print (currNode, connection, tries, connections)
                '''
                print (rects[currNode])
                for n in rects[currNode][1] + rects[currNode][2]:
                    print (n, rects[n])
                '''
        if self.placeNodes == 2:
            for currNode in range(0, len(rects)):
                tries = groupMembers*2
                connections = 2
                while connections and tries:
                    connection = random.randint(0, len(rects)-1)
                    if connection != currNode and not connection in rects[currNode][1] and \
                            not self.testSegmentIntercet(currNode, connection):
                        rects[currNode][1].append(connection)
                        rects[connection][2].append(currNode)
                        connections -= 1
                    tries -= 1

            self.placeNodes = 1
            self.tileMoved = True

        if self.placeNodes == 1:
            self.countdown -= 1
            if self.countdown <= 0:
                self.placeOnCircle()
                self.placeNodes = 0
                self.tileMoved = True
                self.selected = None
                self.mark = None

    # --- events ---
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_running = False
 
            if event.key == pygame.K_SPACE:
                if self.selfSolveCountdown:
                    self.selfSolveCountdown = 0
                else:
                    self.selfSolveCountdown = 1

# ---------------------------------------------------------------------
#
# Mouse drag template is from:
#
# pygame (simple) template - by furas
#
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/
#
# http://pastebin.com/9VdUEPXi
#
# __author__  = 'Bartlomiej "furas" Burek'
# __webpage__ = 'http://blog.furas.pl'
#
# ---------------------------------------------------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # select
                for i, r in enumerate(self.rects):
                    # Pythagoras a^2 + b^2 = c^2
                    dx = r[0].centerx - event.pos[0] # a
                    dy = r[0].centery - event.pos[1] # b
                    distance_square = dx**2 + dy**2 # c^2

                    if distance_square <= int(self.blockSize/2)**2: # c^2 <= radius^2
                        self.selected = i
                        self.selected_offset_x = r[0].x - event.pos[0] # makes the cursor drag at current position
                        self.selected_offset_y = r[0].y - event.pos[1] # not at the top left corner
                        #print ("selected:", i, r[1], r[2])
            if event.button == 3: # mark
                found = False
                for i, r in enumerate(self.rects):
                    # Pythagoras a^2 + b^2 = c^2
                    dx = r[0].centerx - event.pos[0] # a
                    dy = r[0].centery - event.pos[1] # b
                    distance_square = dx**2 + dy**2 # c^2

                    if distance_square <= int(self.blockSize/2)**2: # c^2 <= radius^2
                        if self.mark == i:
                            self.mark = None
                        else:
                            self.mark = i
                        found = True
                        break
                if not found:
                    self.mark = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.selected is not None:
                self.rects[self.selected][0].x = self.myRound(self.rects[self.selected][0].x)
                self.rects[self.selected][0].y = self.myRound(self.rects[self.selected][0].y)
                self.tileMoved = self.selected
                self.selected = None

        elif event.type == pygame.MOUSEMOTION:
            if self.selected is not None: # selected can be `0` so `is not None` is required
                # move object
                self.rects[self.selected][0].x = self.myRound(event.pos[0] + self.selected_offset_x)
                self.rects[self.selected][0].y = self.myRound(event.pos[1] + self.selected_offset_y)

    def on_loop(self):
        # --- updates ---

        self.buildNodesAnimation(self.rects)

        if self.selfSolveCountdown:
            nodeToMove = self.selfSolveOrder[self.selfSolveIndex]
            x = self.rects[nodeToMove][0].x
            y = self.rects[nodeToMove][0].y
            for r in self.rects[nodeToMove][1] + self.rects[nodeToMove][2]:
                x += self.rects[r][0].x
                y += self.rects[r][0].y
            total = 1 + len(self.rects[nodeToMove][1] + self.rects[nodeToMove][2])
            self.rects[nodeToMove][0].topleft = (int(x/total), int(y/total))

            self.selfSolveIndex += 1
            if self.selfSolveIndex == len (self.selfSolveOrder):
                self.selfSolveIndex = 0
                self.selfSolveCountdown -= 1
                random.shuffle(self.selfSolveOrder)
            self.tileMoved = nodeToMove

        if self.tileMoved == True: # test all nodes for intersecting
            self.tileMoved = False
            for i in range(0, len(self.rects)): # a node ...
                self.rects[i][3] = self.colorPalette['nonintersecting']
                for c in self.rects[i][1] + self.rects[i][2]: # ...has connections to
                    if self.testSegmentIntercet(i, c):
                        self.rects[i][3] = self.colorPalette['intersecting']
                        # print ("ALL collides", i, c)
                        break


        if self.tileMoved: # test only moved node ...
            i = self.tileMoved # this node
            self.tileMoved = False
            self.rects[i][3] = self.colorPalette['nonintersecting']
            for c in self.rects[i][1] + self.rects[i][2]: # ...has connections to
                # print (i, c)
                for j in range(0, len(self.rects)): # other nodes...
                    for d in self.rects[j][1] + self.rects[j][2]: #... ande their connections
                        # print (i, c, j, d)
                        if j == i or j == c or d == i or d == c: # but not the node or its connections itself
                            # print ("one of own")
                            pass

                        elif det.doIntersect(self.rects[i][0], self.rects[c][0], self.rects[j][0], self.rects[d][0]): # test if collides
                            self.rects[i][3] = self.colorPalette['intersecting']
                            self.rects[c][3] = self.colorPalette['intersecting']
                            self.rects[j][3] = self.colorPalette['intersecting']
                            self.rects[d][3] = self.colorPalette['intersecting']
                            # print ("ONLY collides", i, c)

            # test if previously intersection node still collides
            for i in range(0, len(self.rects)): # a node ...
                collides = False
                if self.rects[i][3] == self.colorPalette['intersecting']:
                    for c in self.rects[i][1] + self.rects[i][2]: # ...has connections to
                        if self.testSegmentIntercet(i, c):
                            collides = True
                            # print ("PREV collides", i, c)
                            break
                if collides:
                    self.rects[i][3] = self.colorPalette['intersecting']
                else:
                    self.rects[i][3] = self.colorPalette['nonintersecting']

    def draw(self, screen):
        screen.fill(self.colorPalette['background'])

        # draw rect
        for r in self.rects:
            for l in r[1]:
                pygame.draw.line(screen, self.colorPalette['line'], r[0].center, self.rects[l][0].center, 2)
        for i, r in enumerate(self.rects):
            pygame.draw.circle(screen, r[3], r[0].center, int(self.blockSize/2))
            #textToScreen(screen, i, r[0].x, r[0].y, 20, self.colorPalette['line'])

        # draw selected in its color
        if self.selected is not None:
            pygame.draw.circle(screen, self.colorPalette['selected'], self.rects[self.selected][0].center, int(self.blockSize/2))
            for r in self.rects[self.selected][1] + self.rects[self.selected][2]:
                pygame.draw.circle(screen, self.colorPalette['selectedConnecting'], self.rects[r][0].center, int(self.blockSize/2))

        # draw marked with a ring
        if self.mark is not None:
            pygame.draw.circle(screen, self.colorPalette['marked'], self.rects[self.mark][0].center, int(self.blockSize/2), 2)
            for r in self.rects[self.mark][1] + self.rects[self.mark][2]:
                pygame.draw.circle(screen, self.colorPalette['markedConnecting'], self.rects[r][0].center, int(self.blockSize/2), 2)

        pygame.display.update()
        self.clock.tick(25)

if __name__ == "__main__" :
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()
    game = Game()
    running = True
    try:
        while( running and game.getRunningState() ):
            for event in pygame.event.get():
                game.on_event(event)

            game.on_loop()
            game.draw(screen)

    except KeyboardInterrupt:
        running = False
    pygame.quit()

# base example from: https://pythonspot.com/game-development-with-pygame/

#! /usr/bin/env python3
# encoding: utf-8

import pygame
from pygame.locals import *

from games.colorFlood import Game

class App:
 
    windowWidth = 800 # 640
    windowHeight = 600 # 480
    x = 20
    y = 20
    gridSize = 50
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._clock = pygame.time.Clock()
        # self.board = board.Board()
        self.game = Game()
        self.offsetX = 20
        self.offsetY = 20
        # self.board.setBoardDrawArea(self.offsetX, self.offsetY, self.windowWidth - 200, self.windowHeight)
        # self.game.setDrawArea(self.windowWidth - 200, 0, 200, self.windowHeight)
        '''
        boardString = ''
        for i in range(0, len(self.board.board)):
            if i % self.board.x == 0:
                boardString += '\n'
            boardString += str(self.board.board[i])
        print (boardString)
        '''
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
                (self.windowWidth, self.windowHeight), 
                pygame.HWSURFACE)
        self._running = True
        self._image_surf = pygame.image.load("data/images/pygame.png").convert()
        pygame.display.set_caption('Pygame harjoitus')
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == MOUSEBUTTONDOWN:
            # self.board.on_event(event)
            self.game.on_event(event)
 
    def on_loop(self):
        self.game.on_loop()

        if self.game.getRunningState() == False:
            self._running = False
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        # self.board.draw(self._display_surf, self._image_surf)
        self.game.draw(self._display_surf, self._image_surf)
        pygame.display.flip()
        # print (self._clock.get_fps())
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        try:
            while( self._running ):
                for event in pygame.event.get():
                    self.on_event(event)

                pygame.event.pump()
                keys = pygame.key.get_pressed()
     
                if (keys[K_ESCAPE]):
                    self._running = False
 
                if (keys[K_RIGHT] or keys[K_d]):
                    self.offsetX += 20
                    # self.board.setBoardDrawArea(self.offsetX, self.offsetY)
     
                if (keys[K_LEFT] or keys[K_a]):
                    self.offsetX -= 20
                    # self.board.setBoardDrawArea(self.offsetX, self.offsetY)
     
                if (keys[K_UP] or keys[K_w]):
                    self.offsetY -= 20
                    # self.board.setBoardDrawArea(self.offsetX, self.offsetY)
     
                if (keys[K_DOWN] or keys[K_s]):
                    self.offsetY += 20
                    # self.board.setBoardDrawArea(self.offsetX, self.offsetY)

                self.on_loop()
                self.on_render()

                self._clock.tick(30)
        except KeyboardInterrupt:
            self._running = False
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

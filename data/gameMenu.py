#! /usr/bin/env python3
# encoding: utf-8

import pygame
from pygame.locals import *

from data.textToScreen import textToScreen

class MenuItem():
    def __init__(self, text, textSize = 50, textFormat = "{}", value = None, color = [128,0,0],
            padding = 0, uFunc = None, cFunc = None, collideRect = None):
        self.text = text
        self.textSize = textSize
        self.textFormat = textFormat
        self.value = value
        self.color = color
        self.padding = padding
        self.updateFunc = uFunc
        self.clickFunc = cFunc
        self.collideRect = collideRect or Rect(0,0,0,0) # Rect without volume == None
        # print (self.text, self.collideRect, self.clickFunc)

    def update(self):
        if self.updateFunc:
            if self.value == None:
                self.text = self.updateFunc()
            else:
                self.value = self.updateFunc()

    def draw(self, surface):
        if self.value == None:
            textToScreen(surface,
                    self.textFormat.format(self.text),
                    self.collideRect.x, self.collideRect.y,
                    self.textSize, self.color)
        else:
            textToScreen(surface,
                    self.textFormat.format(self.text, self.value),
                    self.collideRect.x, self.collideRect.y,
                    self.textSize, self.color)
        # pygame.draw.rect(surface, [255,255,255], self.collideRect, 2) # Debug position

    def onMouseClick(self):
        if self.collideRect:
            x, y = pygame.mouse.get_pos()
            # print (self.text, self.collideRect, x, y)
            if self.collideRect.collidepoint(x, y):
                if self.clickFunc:
                    self.clickFunc()
                return self.text
        return False

    def setPosition(self, x, y, w = None, h = None):
        self.collideRect.x = x
        self.collideRect.y = y + self.padding
        if h: self.collideRect.height = h
        else: self.collideRect.height = self.textSize
        if w: self.collideRect.width = w
        # print (self.text, self.collideRect, self.clickFunc)
        return self.textSize + self.padding

class MenuContainer():
    def __init__(self, position, active = False, color = None, textPadding = None):
        self.position = position or Rect(0,0,0,0)
        self.textPadding = textPadding or [10,10]
        self.nextItemTop = self.position.top + self.textPadding[1]

        self.active = active
        self.menuItems = []

        self.fill = True
        self.color = color or Color(0,32,0)
        self.border = 2

    def addItem(self, item):
        # print (item)
        if isinstance(item, MenuItem):
            self.nextItemTop += item.setPosition(
                self.position.left + self.textPadding[0],
                self.nextItemTop,
                self.position.width - self.textPadding[0] * 2,
                0)
            self.menuItems.append(item)

    def update(self):
        for i in self.menuItems:
            i.update()

    def draw(self, surface):
        # print (self.color, self.color.correct_gamma(1.25), self.color.correct_gamma(0.75))
        if self.active:
            if self.fill:
                pygame.draw.rect(surface, self.color, self.position, 0)
            if self.border:
                pygame.draw.line(surface, self.color.correct_gamma(1.25),
                    (self.position.x, self.position.y), 
                    (self.position.right, self.position.y), self.border)
                pygame.draw.line(surface, self.color.correct_gamma(1.25),
                    (self.position.x, self.position.y), 
                    (self.position.x, self.position.bottom), self.border)
                pygame.draw.line(surface, self.color.correct_gamma(0.75),
                    (self.position.right - 2, self.position.y),
                    (self.position.right - 2, self.position.bottom - 2), self.border)
                pygame.draw.line(surface, self.color.correct_gamma(0.75),
                    (self.position.x, self.position.bottom - 2),
                    (self.position.right - 2, self.position.bottom - 2), self.border)
            for i in self.menuItems:
                i.draw(surface)

    def onMouseClick(self):
        if self.active:
            x, y = pygame.mouse.get_pos()
            # print (self, self.position, x, y)
            if self.position.collidepoint(x, y):
                for i in self.menuItems:
                    i.onMouseClick()

    def setPassive(self):
        self.active = False

    def setActive(self):
        self.active = True

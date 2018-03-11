#! /usr/bin/env python3
# encoding: utf-8

import os
import sys
import random
import pygame
from pygame.locals import *
import pickle

SCOREPATH = 'data/score'

class HighScore():
    def __init__(self, file = None, scoreAmmount = 10,
            sort1stDescending = False, sort2ndDescending = False):
        self._scoreStateOK = False
        self.file = file
        self.scores = {}
        self.scoreAmmount = scoreAmmount
        self.sort1stDescending = sort1stDescending
        self.sort2ndDescending = sort2ndDescending

        self.readScoreFile()

    def readScoreFile(self):
        try:
            with open(os.path.join(SCOREPATH, self.file + '.pickle'), 'rb') as file:
                self.scores = pickle.load(file)
                self._scoreStateOK = True
        except:
            print("Unexpected error:", sys.exc_info()[0])
            # raise
            pass

    def writeScoreFile(self):
        try:
            with open(os.path.join(SCOREPATH, self.file + '.pickle'), 'wb') as file:
                pickle.dump(self.scores, file)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            # raise
            pass

    def save(self):
        self.writeScoreFile()

    def getScores(self, key):
        if key in self.scores.keys():
            return self.scores[key]
        else:
            return []

    def addScore(self, key, name, score, time = None):
        if key in self.scores.keys():
            self.scores[key].append([name, score, time])
        else:
            self.scores[key] = [[name, score, time]]

        self.scores[key].sort(key=lambda x: (x[2]), reverse=self.sort2ndDescending)
        self.scores[key].sort(key=lambda x: (x[1]), reverse=self.sort1stDescending)

        self.scores[key] = self.scores[key][:self.scoreAmmount]

    def printScores(self, key = None):
        if key:
            for l in self.scores[key]:
                print (l)
        else:
            for key in self.scores.keys():
                print (key)
                for l in self.scores[key]:
                    print (l)


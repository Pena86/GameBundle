#! /usr/bin/env python3
# encoding: utf-8

# Code snipplet from: https://stackoverflow.com/a/20843688

import pygame

def textToScreen(screen, text, x, y, size = 50, color = (200, 000, 000),
        font_type = 'data/fonts/audiowide/Audiowide-Regular.ttf'):

    try:
        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print ('Font Error, saw it coming')
        raise e

# coding=utf-8

import pygame
from pygame.locals import *
from sys import exit

class ScreenPg:
    running = True

    def __init__(self, bg = [25, 25, 25], width = 1000, height = 1000):
        self.pg = pygame
        # Color dle fondo = Casi negro, casi oscuro.
        self.bg = bg
        # Ancho y alto de la pantalla.
        self.width = width
        self.height = height

    def set_mode(self):
        # creación de la pantalla.
        self.screen = self.pg.display.set_mode((self.height, self.width),
                pygame.RESIZABLE |
                pygame.SCALED |
                pygame.HWSURFACE |
                pygame.DOUBLEBUF, 32)

    def set_title(self, title):
        self.pg.display.set_caption(title)

    def draw_polygon(self, color, poins, fill = True):
        self.pg.draw.polygon(self.screen, color, poins, fill)

    def update(self):
        self.pg.display.flip()

    def set_background(self):
        # Pintamos el fondo con el color elegido.
        self.screen.fill(self.bg)

    def quit(self):
        self.pg.quit()

    def beggin(self):
        self.pg.init()
        self.set_mode()
        self.set_background()


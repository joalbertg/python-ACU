import pygame, sys

class ScreenPg:
    running = True

    def __init__(self, bg = [25, 25, 25], width = 500, height = 500):
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
                pygame.DOUBLEBUF, 8)

    def set_background(self):
        # Pintamos el fondo con el color elegido.
        self.screen.fill(self.bg)

    def get_event(self):
        return self.pg.event.get()

    def beggin(self):
        self.pg.init()
        self.set_mode()
        self.set_background()


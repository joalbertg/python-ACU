import pygame
from sys import exit

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

    def set_title(self, title):
        self.pg.display.set_caption(title)

    def draw_polygon(self, color, poins):
        self.pg.draw.polygon(self.screen, color, poins, 1)

    def update(self):
        self.pg.display.flip()

    def set_background(self):
        # Pintamos el fondo con el color elegido.
        self.screen.fill(self.bg)

    ##################################################
    def get_event(self):
        return self.pg.event.get()

    def event_keydown(self, type):
        if type == self.pg.KEYDOWN:
            return True
        return False

    def event_close(self, ev):
        # Detectamos si se presiona esc o hacen click sobre close.
        for event in ev:
            type = event.type
            if (self.event_keydown(type) and event.key == self.pg.K_ESCAPE) \
                    or type == self.pg.QUIT:
                self.pg.quit()
                exit()
    ##################################################
    def is_key(self, key):
        if key in [self.pg.K_UP, self.pg.K_DOWN, self.pg.K_LEFT, self.pg.K_RIGHT, 
                   self.pg.K_n, self.pg.K_m]:
            return True
        return False
    ##################################################

    def beggin(self):
        self.pg.init()
        self.set_mode()
        self.set_background()


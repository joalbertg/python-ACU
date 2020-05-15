# coding=utf-8

import numpy as np

class Fractal:
    def __init__(self, rule = 30, nxC = 500, nyC = 500, width = 500, height = 500):
        self.current_rule(rule) 
        self.nxC = nxC
        self.nyC = nyC
        self.dimCW = width / self.nxC
        self.dimCH = height / self.nyC
        self.reset_game_state()

    def current_rule(self, rule):
        self.rule = rule % (2**(2**3) - 1)

    def up_rule(self):
        self.current_rule(self.rule + 1)

    def down_rule(self):
        self.current_rule(self.rule - 1)

    def up_10_rule(self):
        self.current_rule(self.rule + 10)

    def down_10_rule(self):
        self.current_rule(self.rule - 10)

    def up_height(self, height):
        if (self.nyC + 10) % height == 0:
            self.nyC = 10
        else:
            self.nyC = self.nyC + 10
        self.dimCH = height / self.nyC

    def down_height(self, height):
        if (self.nyC - 10) % height == 0:
            self.nyC = height - 10
        else:
            self.nyC = self.nyC - 10
        self.dimCH = height / self.nyC

    def left_width(self, width):
        if (self.nxC - 10) % width == 0:
            self.nxC = width - 10
        else:
            self.nxC = (self.nxC - 10) % width
        self.dimCW = width / self.nxC

    def right_width(self, width):
        if (self.nxC + 10) % width == 0:
            self.nxC = 10
        else:
            self.nxC = (self.nxC + 10) % width
        self.dimCW = width / self.nxC

    def reset_game_state(self):
        # Estado de las celdas. Vivas = 1, Muertas = 0.
        self.gameState = np.zeros((self.nxC, self.nyC))
        self.gameState[int(self.nxC / 2), 0] = 1

    def binary_rule(self):
        strRule = np.binary_repr(self.rule, 8)
        return np.flip(list(strRule))

    def vector_rule(self):
        return self.binary_rule()

    def x_left(self, x, y):
        return int(self.gameState[(x - 1) % self.nxC, (y) % self.nyC])

    def x_origin(self, x, y):
        return int(self.gameState[(x)     % self.nxC, (y) % self.nyC])

    def x_right(self, x, y):
        return int(self.gameState[(x + 1) % self.nxC, (y) % self.nyC])

    def vicinity(self, x, y):
        # Encontramos los vecinos cercanos de (x, y), (x-1, y)/(x+1, y).
        return "%s%s%s" % (self.x_left(x, y), self.x_origin(x, y), self.x_right(x, y))

    def polygon(self, x, y):
        # Creamos el polself.ígono de cada celda a dibujar.
        return [((x)     * self.dimCW, y       * self.dimCH),
                ((x + 1) * self.dimCW, y       * self.dimCH),
                ((x + 1) * self.dimCW, (y + 1) * self.dimCH),
                ((x)     * self.dimCW, (y + 1) * self.dimCH)]

    def cell_born(self, x, y):
        self.gameState[(x) % self.nxC, (y + 1) % self.nyC] = 1

    def cal_cell(self, x, y):
        return int(self.vector_rule()[int(self.vicinity(x, y), 2)])


import screen_pg
import event_pg
import numpy as np
import time

spg = screen_pg.ScreenPg()
epg = event_pg.EventPg(spg.pg)
spg.beggin()
spg.set_title('Autómatas Celulares: Fractal')

class Fractal:
    def __init__(self, rule = 30, nxC = 500, nyC = 500, width = 500, height = 500):
        self.rule = rule
        self.nxC = nxC
        self.nyC = nyC
        self.dimCW = width / self.nxC
        self.dimCH = height / self.nyC
        self.reset_game_state()

    def up_height(self, height):
        self.nyC = fr.nyC + 10
        self.dimCH = height / self.nyC

    def down_height(self, height):
        self.nyC = fr.nyC - 10
        self.dimCH = height / self.nyC

    def left_width(self, width):
        self.nxC = fr.nxC - 10
        self.dimCW = width / self.nxC

    def right_width(self, width):
        self.nxC = fr.nxC + 10
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
        # Creamos el polfr.ígono de cada celda a dibujar.
        return [((x)     * self.dimCW, y       * self.dimCH),
                ((x + 1) * self.dimCW, y       * self.dimCH),
                ((x + 1) * self.dimCW, (y + 1) * self.dimCH),
                ((x)     * self.dimCW, (y + 1) * self.dimCH)]

    def cell_born(self, x, y):
        self.gameState[(x) % self.nxC, (y + 1) % self.nyC] = 1

    def cal_cell(self, x, y):
        return int(self.vector_rule()[int(self.vicinity(x, y), 2)])

fr = Fractal()

def __log__(msg):
    print('Log:', msg)

def reset():
    fr.reset_game_state()
    spg.screen.fill(spg.bg)

# rule = 110
# rule = 124
# rule = 150
# rule = 90

# Para regla 110
# gameState[nxC -1 , 0] = 1
# Para regla 124
# gameState[0, 0] = 1

# Control de la ejecución del juego.
pauseExect = False
sleep = 0.01
# Para seguir calculando y pintando al reanudar.
x, y = 0, 0
auxY, auxX = 0, 0
painted = False
from sys import exit
# Bucle de ejecición.
while y < fr.nyC or spg.running:
    # Detenemos la ejecución si ya se terminó de pintar.
    if y == fr.nyC:
        painted = True
    # Registramos eventos de teclado y ratón.
    ev = epg.get_event()
    # spg.event_close(ev)
    if epg.event_close(ev):
        spg.quit()
        exit()

    restart = False
    for event in ev:
        if epg.event_keydown(event.type):
            key = event.key

            if spg.is_key(key):
                restart = True
                mods = spg.pg.key.get_mods()

                if key == spg.pg.K_UP:
                    fr.up_height(spg.height)
                elif key == spg.pg.K_DOWN:
                    fr.down_height(spg.height)
                elif key == spg.pg.K_LEFT:
                    fr.left_width(spg.width)
                elif key == spg.pg.K_RIGHT:
                    fr.right_width(spg.width)
                elif key == spg.pg.K_n or key == spg.pg.K_m:
                    if mods & spg.pg.KMOD_LSHIFT or mods & spg.pg.KMOD_CAPS:
                        if key == spg.pg.K_n:
                            fr.rule += 1
                        elif key == spg.pg.K_m:
                            fr.rule += 10
                    elif key == spg.pg.K_n:
                        fr.rule -= 1
                    elif key == spg.pg.K_m:
                        fr.rule -= 10

                painted = False
                y = 0
                auxY = 0
                reset()

    if not painted or not restart:
        for event in ev:
            # Detectamos si se presiona una tecla.
            if epg.event_keydown(event.type) and event.key == spg.pg.K_SPACE:
                pauseExect = not pauseExect

                if auxX == 0 and auxY == 0:
                    auxY, auxX= y, x
                else:
                    y, x = auxY, auxX
                    auxX, auxY = 0, 0

        if not pauseExect:
            time.sleep(sleep)

            for x in range(0, fr.nxC):
                if fr.cal_cell(x, y):
                    fr.cell_born(x, y)
                    spg.draw_polygon((128, 128, 128), fr.polygon(x, y))
            spg.update()
            y += 1

import screen_pg
import numpy as np
import time

spg = screen_pg.ScreenPg()
spg.beggin()
spg.set_title('Autómatas Celulares: Fractal')

class Fractal:
    def __init__(self, sleep = 0.01, nxC = 500, nyC = 500, width = 500, height = 500):
        self.sleep = sleep
        self.nxC = nxC
        self.nyC = nyC
        self.dimCW = width / self.nxC
        self.dimCH = height / self.nyC

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

fr = Fractal()

def reset_cell():
    # Estado de las celdas. Vivas = 1, Muertas = 0.
    return np.zeros((fr.nxC, fr.nyC))

def __log__(msg):
    print('Log:', msg)

def __binary_rule__(rule):
    strRule = np.binary_repr(rule, 8)
    __log__(rule)
    return np.flip(list(strRule))

def __incNyC__(gameState):
    gameState = reset_cell()
    gameState[int(fr.nxC / 2), 0] = 1
    spg.screen.fill(spg.bg)
    return gameState

# Control de la ejecución del juego.
pauseExect = False
rule = 30
# rule = 110
# rule = 124
# rule = 150
# rule = 90

gameState = reset_cell()
gameState[int(fr.nxC / 2), 0] = 1
# Para regla 110
# gameState[nxC -1 , 0] = 1
# Para regla 124
# gameState[0, 0] = 1

vectorRule = __binary_rule__(rule)

x, y = 0, 0
# Para seguir calculando y pintando al reanudar.
auxY, auxX = 0, 0
painted = False
from sys import exit
# Bucle de ejecición.
# while True:


while y < fr.nyC or spg.running:
    # Detenemos la ejecución si ya se terminó de pintar.
    if y == fr.nyC:
        painted = True
    # Registramos eventos de teclado y ratón.
    ev = spg.get_event()
    spg.event_close(ev)

    restart = False
    for event in ev:
        if spg.event_keydown(event.type):
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
                            rule += 1
                        elif key == spg.pg.K_m:
                            rule += 10
                    elif key == spg.pg.K_n:
                        rule -= 1
                    elif key == spg.pg.K_m:
                        rule -= 10

                    vectorRule = __binary_rule__(rule)

                painted = False
                y = 0
                auxY = 0
                gameState = __incNyC__(gameState)

    if not painted or not restart:
        for event in ev:
            # Detectamos si se presiona una tecla.
            if spg.event_keydown(event.type) and event.key == spg.pg.K_SPACE:
                pauseExect = not pauseExect

                if auxX == 0 and auxY == 0:
                    auxY, auxX= y, x
                else:
                    y, x = auxY, auxX
                    auxX, auxY = 0, 0

        if not pauseExect:
            time.sleep(fr.sleep)

            for x in range(0, fr.nxC):
                # Encontramos los vecinos cercanos, (x-1, y)/(x+1, y).
                xLeft   = int(gameState[(x - 1) % fr.nxC, (y) % fr.nyC])
                xOrigin = int(gameState[(x)     % fr.nxC, (y) % fr.nyC])
                xRight  = int(gameState[(x + 1) % fr.nxC, (y) % fr.nyC])

                vicinity = "%s%s%s" % (xLeft, xOrigin, xRight)
                cell = int(vectorRule[int(vicinity, 2)])

                if cell:
                    gameState[(x) % fr.nxC, (y + 1) % fr.nyC] = 1

                    # Creamos el polfr.ígono de cada celda a dibujar.
                    poly = [((x)     * fr.dimCW, y       * fr.dimCH),
                            ((x + 1) * fr.dimCW, y       * fr.dimCH),
                            ((x + 1) * fr.dimCW, (y + 1) * fr.dimCH),
                            ((x)     * fr.dimCW, (y + 1) * fr.dimCH)]
                    # Y dibujamos la celda para el par de x e y.
                    spg.draw_polygon((128, 128, 128), poly)
            spg.update()
            y += 1

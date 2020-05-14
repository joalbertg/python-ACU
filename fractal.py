import screen_pg
import numpy as np
import time

spg = screen_pg.ScreenPg()
spg.beggin()

# spg.pg.display.set_caption('Autómatas Celulares: Fractal')
spg.pg.display.set_caption('Autómatas Celulares: Fractal')

nxC, nyC = 500, 500

dimCW = spg.width / nxC
dimCH = spg.height / nyC

# Estado de las celdas. Vivas = 1, Muertas = 0.
gameState = np.zeros((nxC, nyC))

def __incNyC__(gameState):
    gameState = np.zeros((nxC, nyC))
    gameState[int(nxC / 2), 0] = 1
    spg.screen.fill(spg.bg)

    return gameState

gameState[int(nxC / 2), 0] = 1
# Para regla 110
# gameState[nxC -1 , 0] = 1
# Para regla 124
# gameState[0, 0] = 1

# Control de la ejecución del juego.
pauseExect = False
sleep = 0.01
rule = 30
# rule = 110
# rule = 124
# rule = 150
# rule = 90
def __log__(msg):
    print('Log:', msg)

def __binary_rule__(rule):
    strRule = np.binary_repr(rule, 8)
    __log__(rule)
    return np.flip(list(strRule))

vectorRule = __binary_rule__(rule)
def exit_event(ev):
    for event in ev:
        # Detectamos si se presiona esc o hacen click sobre close.
        if (event.type == spg.pg.KEYDOWN and event.key == spg.pg.K_ESCAPE) \
        or (event.type == spg.pg.QUIT):
            spg.pg.quit()
            exit()

x, y = 0, 0
# Para seguir calculando y pintando al reanudar.
auxY, auxX = 0, 0
painted = False
from sys import exit
# Bucle de ejecición.
# while True:
while y < nyC or spg.running:
    # Detenemos la ejecución si ya se terminó de pintar.
    if y == nyC:
        painted = True
    # Registramos eventos de teclado y ratón.
    ev = spg.pg.event.get()

    exit_event(ev)

    restart = False
    for event in ev:
        if event.type == spg.pg.KEYDOWN:
            key = event.key

            if key == spg.pg.K_UP or key == spg.pg.K_DOWN or key == spg.pg.K_LEFT or key == spg.pg.K_RIGHT \
                    or key == spg.pg.K_n or key == spg.pg.K_m:
                restart = True
                mods = spg.pg.key.get_mods()

                if key == spg.pg.K_UP:
                    nyC = nyC + 10
                    dimCH = spg.height / nyC
                elif key == spg.pg.K_DOWN:
                    nyC = nyC - 10
                    dimCH = spg.height / nyC
                elif key == spg.pg.K_LEFT:
                    nxC = nxC - 10
                    dimCW = spg.width / nxC
                elif key == spg.pg.K_RIGHT:
                    nxC = nxC + 10
                    dimCW = spg.width / nxC
                elif key == spg.pg.K_n:
                    if mods & spg.pg.KMOD_LSHIFT or mods & spg.pg.KMOD_CAPS:
                        rule += 1
                    else:
                        rule -= 1

                    vectorRule = __binary_rule__(rule)
                elif key == spg.pg.K_m:
                    if mods & spg.pg.KMOD_LSHIFT or mods & spg.pg.KMOD_CAPS:
                        rule += 10
                    else:
                        rule -= 10

                    vectorRule = __binary_rule__(rule)

                painted = False
                y = 0
                auxY = 0
                gameState = __incNyC__(gameState)

    if not painted or not restart:
        for event in ev:
            # Detectamos si se presiona una tecla.
            if event.type == spg.pg.KEYDOWN and event.key == spg.pg.K_SPACE:
                pauseExect = not pauseExect

                if auxX == 0 and auxY == 0:
                    auxY, auxX= y, x
                else:
                    y, x = auxY, auxX
                    auxX, auxY = 0, 0

        if not pauseExect:
            time.sleep(sleep)

            for x in range(0, nxC):
                # Encontramos los vecinos cercanos, (x-1, y)/(x+1, y).
                xLeft   = int(gameState[(x - 1) % nxC, (y) % nyC])
                xOrigin = int(gameState[(x)     % nxC, (y) % nyC])
                xRight  = int(gameState[(x + 1) % nxC, (y) % nyC])

                vicinity = "%s%s%s" % (xLeft, xOrigin, xRight)
                cell = int(vectorRule[int(vicinity, 2)])

                if cell:
                    gameState[(x) % nxC, (y + 1) % nyC] = 1

                    # Creamos el polígono de cada celda a dibujar.
                    poly = [((x)     * dimCW, y       * dimCH),
                            ((x + 1) * dimCW, y       * dimCH),
                            ((x + 1) * dimCW, (y + 1) * dimCH),
                            ((x)     * dimCW, (y + 1) * dimCH)]
                    # Y dibujamos la celda para el par de x e y.
                    spg.pg.draw.polygon(spg.screen, (128, 128, 128), poly, 1)
            spg.pg.display.flip()
            y += 1

import pygame
import numpy as np
import time

pygame.init()

pygame.display.set_caption('Autómatas Celulares: Fractal')

# Ancho y alto de la pantalla.
width, height = 1000, 1000
# creación de la pantalla.
screen = pygame.display.set_mode(
        (height, width),
        pygame.RESIZABLE |
        pygame.SCALED |
        pygame.HWSURFACE |
        pygame.DOUBLEBUF,
        8)

# Color dle fondo = Casi negro, casi oscuro.
bg = 25, 25, 25
# Pintamos el fondo con el color elegido.
screen.fill(bg)

nxC, nyC = 500, 500

dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1, Muertas = 0.
gameState = np.zeros((nxC, nyC))

def __incNyC__(gameState):
    gameState = np.zeros((nxC, nyC))
    gameState[int(nxC / 2), 0] = 1
    screen.fill(bg)

    return gameState

gameState[int(nxC / 2), 0] = 1
# Para regla 110
# gameState[nxC -1 , 0] = 1
# Para regla 124
# gameState[0, 0] = 1

# Control de la ejecución del juego.
running = True
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
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
        or (event.type == pygame.QUIT):
            pygame.quit()
            exit()

x, y = 0, 0
# Para seguir calculando y pintando al reanudar.
auxY, auxX = 0, 0
painted = False
from sys import exit
# Bucle de ejecición.
# while True:
while y < nyC or running:
    # Detenemos la ejecución si ya se terminó de pintar.
    if y == nyC:
        painted = True
    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    exit_event(ev)

    restart = False
    for event in ev:
        if event.type == pygame.KEYDOWN:
            key = event.key

            if key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT \
                    or key == pygame.K_n or key == pygame.K_m:
                restart = True
                mods = pygame.key.get_mods()

                if key == pygame.K_UP:
                    nyC = nyC + 10
                    dimCH = height / nyC
                elif key == pygame.K_DOWN:
                    nyC = nyC - 10
                    dimCH = height / nyC
                elif key == pygame.K_LEFT:
                    nxC = nxC - 10
                    dimCW = width / nxC
                elif key == pygame.K_RIGHT:
                    nxC = nxC + 10
                    dimCW = width / nxC
                elif key == pygame.K_n:
                    if mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_CAPS:
                        rule += 1
                    else:
                        rule -= 1

                    vectorRule = __binary_rule__(rule)
                elif key == pygame.K_m:
                    if mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_CAPS:
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            pygame.display.flip()
            y += 1

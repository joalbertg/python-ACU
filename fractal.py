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

common = 450
nxC, nyC = common, common

dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1, Muertas = 0.
gameState = np.zeros((nxC, nyC))

gameState[int(nxC / 2), 0] = 1
# Para regla 110
# gameState[nxC -1 , 0] = 1
# Para regla 124
# gameState[0, 0] = 1

# Control de la ejecución del juego.
running = True
pauseExect = False
sleep = 0.01
# rule = 30
# rule = 110
# rule = 124
# rule = 150
rule = 90
strRule = np.binary_repr(rule, 8)
vectorRule = np.flip(list(strRule))

def exit_event(ev):
    for event in ev:
        # Detectamos si se presiona esc o hacen click sobre close.
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
        or (event.type == pygame.QUIT):
            pygame.quit()
            exit()

y = 0
# Para seguir calculando y pintando al reanudar.
auxY, auxX = 0, 0
painted = False
from sys import exit
# Bucle de ejecición.
# while True:
while y < nxC or running:
    # Detenemos la ejecución si ya se terminó de pintar.
    if y == nyC:
        painted = True
    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    exit_event(ev)

    if not painted:
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

            for x in range(0, nyC):
                # Encontramos los vecinos cercanos, (x-1, y)/(x+1, y).
                xLeft =  int(gameState[(x - 1) % nxC, (y) % nyC])
                xOrigin = int(gameState[x % nxC, y % nyC])
                xRight = int(gameState[(x + 1) % nxC, (y) % nyC])

                vicinity = "%s%s%s" % (xLeft, xOrigin, xRight)
                cell = int(vectorRule[int(vicinity, 2)])

                if cell:
                    gameState[x, (y + 1) % nyC] = 1

                    # Creamos el polígono de cada celda a dibujar.
                    poly = [((x)     * dimCW, y       * dimCH),
                            ((x + 1) * dimCW, y       * dimCH),
                            ((x + 1) * dimCW, (y + 1) * dimCH),
                            ((x)     * dimCW, (y + 1) * dimCH)]
                    # Y dibujamos la celda para el par de x e y.
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            pygame.display.flip()
            y += 1

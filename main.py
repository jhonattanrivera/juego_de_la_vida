import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la pantalla
width, height = 600, 600
screen = pygame.display.set_mode((height, width))

# Color de fondo
bg = 25, 25, 25
screen.fill(bg)

# Tamaño de las celdas
nxC, nyC = 50, 50
dimCW = width  / nxC
dimCH = height / nyC

# Células 'vivas' = 1 y 'muertas' = 0
gameState = np.zeros((nxC, nyC))

# Autómata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Autómata móvil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control de la ejecución
pauseExect = False

# Bucle de ejecución
while True:
    newGameState = np.copy(gameState)
    screen.fill(bg)
    #time.sleep(0.1)

    # Registro de taclado y ratón
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range (0, nxC):
        for x in range(0, nyC):
            if not pauseExect:
                # Calcula el número de celdas 'vecinas'
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                        gameState[(x)   % nxC, (y-1) % nyC] + \
                        gameState[(x+1) % nxC, (y-1) % nyC] + \
                        gameState[(x-1) % nxC, (y)   % nyC] + \
                        gameState[(x+1) % nxC, (y)   % nyC] + \
                        gameState[(x-1) % nxC, (y+1) % nyC] + \
                        gameState[(x)   % nxC, (y+1) % nyC] + \
                        gameState[(x+1) % nxC, (y+1) % nyC]

                # REGLA 1: Una célula muerta con exactamente 3 'vecinas' vivas, 'revive'
                if ((gameState[x, y] == 0) and (n_neigh == 3)):
                    newGameState[x, y] = 1
                
                #REGLA 2: Una célcula viva con menos de 2 o 3 'vecinas' vivas, 'muere'
                elif ((gameState[x, y] == 1) and (n_neigh < 2 or n_neigh > 3)):
                    newGameState[x ,y] = 0

            # Crea el polígono de cada celda a dibujar
            poly = [((x)   * dimCW, y     * dimCH),
                    ((x+1) * dimCW, y     * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]
            
            # Dibuja la celda para cada par de x, y
            if (newGameState[x, y] == 0):
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    
    # Actualiza el estado del juego
    gameState = np.copy(newGameState)

    # Actualiza la pantalla
    pygame.display.flip()
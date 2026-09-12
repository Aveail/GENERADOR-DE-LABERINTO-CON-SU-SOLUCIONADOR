import pygame
import random
from collections import deque

# Inicialización de Pygame
pygame.init()

# Parámetros
tamaño_celdas = 20
filas, columnas = 25, 25

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Crear pantalla
screen = pygame.display.set_mode((columnas * tamaño_celdas, filas * tamaño_celdas))
pygame.display.set_caption("Generador y Solucionador de Laberintos")

# Generador de laberinto con algoritmo DFS
def generar_laberinto(filas, columnas):
    laberinto = [[1 for _ in range(columnas)] for _ in range(filas)]
    stack = [(1, 1)]
    laberinto[1][1] = 0

    while stack:
        x, y = stack[-1]
        vecinos = []
        for dx, dy in [(0,2),(0,-2),(2,0),(-2,0)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx < filas-1 and 1 <= ny < columnas-1 and laberinto[nx][ny] == 1:
                vecinos.append((nx, ny, dx, dy))
        if vecinos:
            nx, ny, dx, dy = random.choice(vecinos)
            laberinto[nx][ny] = 0
            laberinto[x+dx//2][y+dy//2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    # Entrada y salida
    laberinto[1][1] = 2   # jugador
    laberinto[filas-2][columnas-2] = 3  # meta
    return laberinto

# Solucionador con BFS
def resolver_laberinto(laberinto):
    start = None
    end = None
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 2:
                start = (i,j)
            elif laberinto[i][j] == 3:
                end = (i,j)

    queue = deque([start])
    visited = {start: None}

    while queue:
        x,y = queue.popleft()
        if (x,y) == end:
            break
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]):
                if laberinto[nx][ny] in (0,3) and (nx,ny) not in visited:
                    visited[(nx,ny)] = (x,y)
                    queue.append((nx,ny))

    # Reconstruir camino
    camino = []
    nodo = end
    while nodo:
        camino.append(nodo)
        nodo = visited.get(nodo)
    camino.reverse()
    return camino

# Dibujar laberinto
def draw_laberinto(laberinto, camino=None):
    for row in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            color = WHITE
            if laberinto[row][col] == 1:
                color = BLACK
            elif laberinto[row][col] == 2:
                color = GREEN
            elif laberinto[row][col] == 3:
                color = RED
            pygame.draw.rect(screen, color, (col*tamaño_celdas, row*tamaño_celdas, tamaño_celdas, tamaño_celdas))

    # Dibujar camino solucionador
    if camino:
        for (x,y) in camino:
            pygame.draw.rect(screen, BLUE, (y*tamaño_celdas, x*tamaño_celdas, tamaño_celdas, tamaño_celdas))

# Bucle principal
def main():
    laberinto = generar_laberinto(filas, columnas)
    camino = resolver_laberinto(laberinto)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_laberinto(laberinto, camino)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
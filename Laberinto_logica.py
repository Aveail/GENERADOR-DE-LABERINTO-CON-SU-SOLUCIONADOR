## Andy
import random
from collections import deque


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


def resolver_laberinto(laberinto):
    start = None
    end = None
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 2:
                start = (i,j)
            elif laberinto[i][j] == 3:
                end = (i,j)

    if not start or not end:
        return []

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

    camino = []
    nodo = end
    while nodo:
        camino.append(nodo)
        nodo = visited.get(nodo)
    camino.reverse()
    return camino
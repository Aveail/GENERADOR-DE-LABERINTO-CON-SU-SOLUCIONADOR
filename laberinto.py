import pygame
import random
from collections import deque
import time

pygame.init()

# Parámetros
tamaño_celdas = 25
filas, columnas = 25, 25
tiempo_limite = 20  # segundos

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pantalla (+50 píxeles arriba para el contador)
screen = pygame.display.set_mode((columnas * tamaño_celdas, filas * tamaño_celdas + 50))
pygame.display.set_caption("Proyecto Laberinto")

font = pygame.font.Font(None, 36)

# Generador de laberinto
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

# Resolver con BFS
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
            pygame.draw.rect(screen, color, (col*tamaño_celdas, row*tamaño_celdas+50, tamaño_celdas, tamaño_celdas))

    if camino:
        for (x,y) in camino:
            pygame.draw.rect(screen, BLUE, (y*tamaño_celdas, x*tamaño_celdas+50, tamaño_celdas, tamaño_celdas))

# Obtener posición del jugador
def get_player(laberinto):
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 2:
                return i,j

# Mover jugador
def move_player(laberinto, dx, dy):
    x,y = get_player(laberinto)
    nx, ny = x+dx, y+dy
    if 0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]):
        if laberinto[nx][ny] == 0:  # camino
            laberinto[x][y] = 0
            laberinto[nx][ny] = 2
        elif laberinto[nx][ny] == 3:  # meta
            laberinto[x][y] = 0
            laberinto[nx][ny] = 2  # jugador entra en la meta
            return True
    return False

# ==========================================================
# NUEVA FUNCIÓN: DIBUJAR CUADRO DE NIVEL SUPERADO
# ==========================================================

def dibujar_menu_nivel(nivel, derrota=False):

    ancho_cuadro = 500
    alto_cuadro = 250

    x_cuadro = (
        columnas * tamaño_celdas - ancho_cuadro
    ) // 2

    y_cuadro = (
        filas * tamaño_celdas + 50 - alto_cuadro
    ) // 2

    # Cuadro principal
    pygame.draw.rect(
        screen,
        (40, 40, 40),
        (x_cuadro, y_cuadro, ancho_cuadro, alto_cuadro)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (x_cuadro, y_cuadro, ancho_cuadro, alto_cuadro),
        3
    )

    # Título
    if derrota:
        titulo = font.render(
            "¡Se acabó el tiempo!",
            True,
            WHITE
        )
    else:
        titulo = font.render(
            f"¡Nivel {nivel} completado!",
            True,
            WHITE
        )

    screen.blit(
        titulo,
        (
            x_cuadro + (ancho_cuadro - titulo.get_width()) // 2,
            y_cuadro + 50
        )
    )

    # Botones
    boton_izquierdo = pygame.Rect(
        x_cuadro + 70,
        y_cuadro + 130,
        160,
        55
    )

    boton_derecho = pygame.Rect(
        x_cuadro + 270,
        y_cuadro + 130,
        160,
        55
    )

    if derrota:

        # Botón RESOLVER
        pygame.draw.rect(
            screen,
            GREEN,
            boton_izquierdo
        )

        texto_resolver = font.render(
            "RESOLVER",
            True,
            WHITE
        )

        screen.blit(
            texto_resolver,
            (
                boton_izquierdo.centerx - texto_resolver.get_width() // 2,
                boton_izquierdo.centery - texto_resolver.get_height() // 2
            )
        )

    else:

        # Botón CONTINUAR
        pygame.draw.rect(
            screen,
            GREEN,
            boton_izquierdo
        )

        texto_continuar = font.render(
            "CONTINUAR",
            True,
            WHITE
        )

        screen.blit(
            texto_continuar,
            (
                boton_izquierdo.centerx - texto_continuar.get_width() // 2,
                boton_izquierdo.centery - texto_continuar.get_height() // 2
            )
        )

    # Botón SALIR
    pygame.draw.rect(
        screen,
        RED,
        boton_derecho
    )

    texto_salir = font.render(
        "SALIR",
        True,
        WHITE
    )

    screen.blit(
        texto_salir,
        (
            boton_derecho.centerx - texto_salir.get_width() // 2,
            boton_derecho.centery - texto_salir.get_height() // 2
        )
    )

    return boton_izquierdo, boton_derecho

   


# Bucle principal
def main():
    laberinto = generar_laberinto(filas, columnas)
    camino = resolver_laberinto(laberinto)

    start_time = time.time()
    running = True
    mostrar_solucion = False
    victoria = False
    derrota = False

    # Nivel y récord
    nivel = 1
    record = 1

    # Para saber si estamos mostrando el menú de nivel
    mostrar_menu_nivel = False
    mostrar_menu_derrota = False

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # ==========================================
            # MOVIMIENTO DEL JUGADOR
            # ==========================================

            elif event.type == pygame.KEYDOWN and not victoria and not derrota and not mostrar_menu_nivel:

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    victoria = move_player(laberinto, -1, 0)

                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    victoria = move_player(laberinto, 1, 0)

                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    victoria = move_player(laberinto, 0, -1)

                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    victoria = move_player(laberinto, 0, 1)

                # Si ganó el nivel
                if victoria:
                    record = max(record, nivel)
                    mostrar_menu_nivel = True

            # ==========================================
            # BOTONES DEL MENÚ
            # ==========================================

            elif event.type == pygame.MOUSEBUTTONDOWN:

                 # ==========================================
                 # MENÚ CUANDO GANA
                 # ==========================================
             
                 if event.button == 1 and mostrar_menu_nivel:
             
                     ancho_cuadro = 500
                     alto_cuadro = 250
             
                     x_cuadro = (
                         columnas * tamaño_celdas - ancho_cuadro
                     ) // 2
             
                     y_cuadro = (
                         filas * tamaño_celdas + 50 - alto_cuadro
                     ) // 2
             
                     # Botón CONTINUAR
                     boton_continuar = pygame.Rect(
                         x_cuadro + 70,
                         y_cuadro + 130,
                         160,
                         55
                     )
             
                     # Botón SALIR
                     boton_salir = pygame.Rect(
                         x_cuadro + 270,
                         y_cuadro + 130,
                         160,
                         55
                     )
             
                     # CONTINUAR
                     if boton_continuar.collidepoint(event.pos):
             
                         nivel += 1
             
                         laberinto = generar_laberinto(
                             filas,
                             columnas
                         )
             
                         camino = resolver_laberinto(
                             laberinto
                         )
             
                         start_time = time.time()
             
                         victoria = False
                         derrota = False
                         mostrar_solucion = False
                         mostrar_menu_nivel = False
             
                     # SALIR
                     elif boton_salir.collidepoint(event.pos):
             
                         running = False
             
             
                 # ==========================================
                 # MENÚ CUANDO PIERDE
                 # ==========================================
             
                 elif event.button == 1 and mostrar_menu_derrota:
             
                     ancho_cuadro = 500
                     alto_cuadro = 250
             
                     x_cuadro = (
                         columnas * tamaño_celdas - ancho_cuadro
                     ) // 2
             
                     y_cuadro = (
                         filas * tamaño_celdas + 50 - alto_cuadro
                     ) // 2
             
                     # Botón RESOLVER
                     boton_resolver = pygame.Rect(
                         x_cuadro + 70,
                         y_cuadro + 130,
                         160,
                         55
                     )
             
                     # Botón SALIR
                     boton_salir = pygame.Rect(
                         x_cuadro + 270,
                         y_cuadro + 130,
                         160,
                         55
                     )
             
                     # RESOLVER
                     if boton_resolver.collidepoint(event.pos):
             
                         mostrar_solucion = True
                         mostrar_menu_derrota = False
             
                     # SALIR
                     elif boton_salir.collidepoint(event.pos):
             
                         running = False
                                     

        # ==============================================
        # ACTUALIZAR TIEMPO
        # ==============================================

        if not victoria and not derrota and not mostrar_menu_nivel:

            elapsed = time.time() - start_time

            tiempo_restante = max(
                0,
                tiempo_limite - int(elapsed)
            )

        else:

            # Congelar el contador
            tiempo_restante = tiempo_restante

        # ==============================================
        # DIBUJAR PANTALLA
        # ==============================================

        screen.fill(WHITE)

        # Tiempo
        texto = font.render(
            f"Tiempo: {tiempo_restante}",
            True,
            BLACK
        )

        screen.blit(
            texto,
            (10, 10)
        )

        # Nivel actual
        texto_nivel = font.render(
            f"Nivel: {nivel}",
            True,
            BLACK
        )

        screen.blit(
            texto_nivel,
            (200, 10)
        )

        # Récord
        texto_record = font.render(
            f"Record: Nivel {record}",
            True,
            BLACK
        )

        screen.blit(
            texto_record,
            (330, 10)
        )

        # ==============================================
        # DERROTA POR TIEMPO
        # ==============================================

        if tiempo_restante == 0 and not victoria and not derrota:
             derrota = True
             mostrar_menu_derrota = True

        # ==============================================
        # MENSAJE DE VICTORIA
        # ==============================================

        if victoria:

            texto_victoria = font.render(
                "",
                True,
                (0, 128, 0)
            )

            screen.blit(
                texto_victoria,
                (200, 10)
            )

        # ==============================================
        # MENSAJE DE DERROTA
        # ==============================================

        if derrota:

            texto_derrota = font.render(
                "",
                True,
                (200, 0, 0)
            )

            screen.blit(
                texto_derrota,
                (200, 10)
            )

        # ==============================================
        # DIBUJAR LABERINTO
        # ==============================================

        draw_laberinto(
            laberinto,
            camino if mostrar_solucion else None
        )

        # ==============================================
        # MOSTRAR MENÚ DE NIVEL
        # ==============================================

        if mostrar_menu_nivel:

            dibujar_menu_nivel(nivel)

        if mostrar_menu_derrota:
            dibujar_menu_nivel(nivel, True)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import time

from Niveles import NIVELES
from Laberinto_logica import generar_laberinto, resolver_laberinto

pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Espacios :)
CONTADOR_HEIGHT = 60
BUTTON_AREA_HEIGHT = 50

AREA_JUEGO_ANCHO = 420
AREA_JUEGO_ALTO = 420

tamaño_celdas = 20

font = pygame.font.Font(None, 36)


# Dibujar laberinto
def draw_laberinto(screen, laberinto, camino=None):
    for row in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            color = WHITE
            if laberinto[row][col] == 1:
                color = BLACK
            elif laberinto[row][col] == 2:
                color = GREEN
            elif laberinto[row][col] == 3:
                color = RED
            pygame.draw.rect(screen, color, (col*tamaño_celdas, row*tamaño_celdas+CONTADOR_HEIGHT, tamaño_celdas, tamaño_celdas))

    if camino:
        for (x,y) in camino:
            pygame.draw.rect(screen, BLUE, (y*tamaño_celdas, x*tamaño_celdas+CONTADOR_HEIGHT, tamaño_celdas, tamaño_celdas))

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


# Bucle de un nivel. Devuelve "siguiente", "reiniciar" o "salir".
def jugar_nivel(numero_nivel, config, es_ultimo_nivel):
    global tamaño_celdas

    filas = config["filas"]
    columnas = config["columnas"]
    tiempo_limite = config["tiempo"]

    # La celda se achica según cuántas filas/columnas tenga el nivel,
    # así el laberinto siempre ocupa el mismo espacio en pantalla.
    tamaño_celdas = min(AREA_JUEGO_ANCHO // columnas, AREA_JUEGO_ALTO // filas)

    ancho_ventana = AREA_JUEGO_ANCHO
    alto_ventana = AREA_JUEGO_ALTO + CONTADOR_HEIGHT + BUTTON_AREA_HEIGHT
    screen = pygame.display.set_mode((ancho_ventana, alto_ventana))
    pygame.display.set_caption(f"Proyecto Laberinto - Nivel {numero_nivel + 1}")

    buttons_y = CONTADOR_HEIGHT + AREA_JUEGO_ALTO + 10
    boton_reiniciar = pygame.Rect(50, buttons_y-5, 160, 40)
    boton_solucion  = pygame.Rect(220, buttons_y-5, 160, 40)
    boton_siguiente = pygame.Rect(220, buttons_y-5, 160, 40)

    laberinto = generar_laberinto(filas, columnas)
    camino = resolver_laberinto(laberinto)

    start_time = time.time()
    running = True
    mostrar_solucion = False
    victoria = False
    derrota = False
    tiempo_restante = tiempo_limite
    last_move_time = 0
    move_delay = 110

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if victoria or derrota:
                    if boton_reiniciar.collidepoint(event.pos):
                        return "reiniciar"
                if derrota:
                    if boton_solucion.collidepoint(event.pos):
                        mostrar_solucion = not mostrar_solucion
                if victoria:
                    if boton_siguiente.collidepoint(event.pos):
                        return "salir" if es_ultimo_nivel else "siguiente"

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        if not victoria and not derrota and now - last_move_time >= move_delay:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                victoria = move_player(laberinto, -1, 0)
                last_move_time = now
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                victoria = move_player(laberinto, 1, 0)
                last_move_time = now
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                victoria = move_player(laberinto, 0, -1)
                last_move_time = now
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                victoria = move_player(laberinto, 0, 1)
                last_move_time = now

        if not victoria and not derrota:
            elapsed = time.time() - start_time
            tiempo_restante = max(0, tiempo_limite - int(elapsed))

        if tiempo_restante == 0 and not victoria:
            derrota = True

        screen.fill(WHITE)
        texto = font.render(f"Nivel {numero_nivel + 1}   Tiempo: {tiempo_restante}", True, BLACK)
        screen.blit(texto, (10, 10))

        if victoria:
            msg = "¡Completaste todos los niveles!" if es_ultimo_nivel else "¡¡¡Ganaste!!!"
            texto_victoria = font.render(msg, True, (0,128,0))
            screen.blit(texto_victoria, (15, 35)) #texto para victoria 
            pygame.draw.rect(screen, (60, 70, 200), boton_reiniciar)
            texto_btn1 = font.render("Reiniciar", True, WHITE)
            screen.blit(texto_btn1, (boton_reiniciar.x + 28, boton_reiniciar.y + 8))
            if not es_ultimo_nivel:
                pygame.draw.rect(screen, (60, 150, 70), boton_siguiente)
                texto_btn2 = font.render("Siguiente", True, WHITE)
                screen.blit(texto_btn2, (boton_siguiente.x + 23, boton_siguiente.y + 8))

        if derrota:
            texto_derrota = font.render("¡Perdiste :(!", True, (200,0,0))
            screen.blit(texto_derrota, (10, 33)) #texto para derrota
            pygame.draw.rect(screen, (60, 70, 200), boton_reiniciar)
            pygame.draw.rect(screen, (60, 150, 70), boton_solucion)
            texto_btn1 = font.render("Reiniciar", True, WHITE)
            texto_btn2 = font.render("Solución", True, WHITE)
            screen.blit(texto_btn1, (boton_reiniciar.x + 28, boton_reiniciar.y + 8))
            screen.blit(texto_btn2, (boton_solucion.x + 23, boton_solucion.y + 8))

        draw_laberinto(screen, laberinto, camino if mostrar_solucion else None)
        pygame.display.flip()

    return "salir"


def main():
    nivel_actual = 0
    resultado = "reiniciar"

    while resultado in ("reiniciar", "siguiente"):
        nivel_actual = min(nivel_actual, len(NIVELES) - 1)
        es_ultimo_nivel = nivel_actual == len(NIVELES) - 1
        resultado = jugar_nivel(nivel_actual, NIVELES[nivel_actual], es_ultimo_nivel)

        if resultado == "siguiente":
            nivel_actual += 1
            resultado = "reiniciar"  # para que el while siga iterando al nuevo nivel

    pygame.quit()


if __name__ == "__main__":
    main()
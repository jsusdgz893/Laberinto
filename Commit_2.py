
import os
import time

def limpiar_pantalla():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Unix-based (Linux, macOS)
    else:
        os.system('clear')


# Definimos el laberinto con características especiales
laberinto = [
    [0, 1, 1, 0, 0, 3],  # 3 es teletransporte a 4
    [0, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 111, 0],  # 111 requiere resolver una trivia
    [1, 1, 1, 1, 1, 0],
    [4, 0, 0, 0, 0, 2]  # 4 es teletransporte a 3, 2 es la salida
]

# Coordenadas de entrada y salida
entrada = (0, 0)
salida = (5, 5)

# Función para verificar si una celda es válida (dentro del laberinto y no es una pared)
def es_valida(x, y):
    return 0 <= x < len(laberinto) and 0 <= y < len(laberinto[0]) and laberinto[x][y] != 1

# Función para resolver la trivia de la celda 111
def resolver_trivia():
    print("¡Has llegado a la celda misteriosa 111! Responde la pregunta para continuar.")
    pregunta = "¿Cuál es el número primo más pequeño?"
    respuesta_correcta = "2"
    respuesta = input(f"{pregunta} ")
    return respuesta == respuesta_correcta

# Imprimir el laberinto con la posición actual marcada
def imprimir_laberinto(laberinto, posicion_actual):
    for i, fila in enumerate(laberinto):
        fila_imprimible = []
        for j, celda in enumerate(fila):
            if (i, j) == posicion_actual:
                fila_imprimible.append("X")  # Marca la posición actual
            else:
                fila_imprimible.append(celda)
        print(fila_imprimible)
    print()  # Línea en blanco para mejor visualización

# Algoritmo de programación dinámica para encontrar el camino
def encontrar_camino(laberinto, entrada, salida):
    n = len(laberinto)
    dp = [[None for _ in range(len(laberinto[0]))] for _ in range(n)]  # Matriz para almacenar soluciones parciales
    return buscar_camino(laberinto, entrada[0], entrada[1], salida, dp)

# Función recursiva que busca el camino usando programación dinámica
def buscar_camino(laberinto, x, y, salida, dp):
    # Si hemos llegado a la salida
    if (x, y) == salida:
        return [(x, y)]

    # Si la celda es inválida o ya fue visitada
    if not es_valida(x, y) or dp[x][y] is not None:
        return None

    # Si llegamos a la celda 111, resolvemos la trivia
    if laberinto[x][y] == 111:
        if not resolver_trivia():
            print("Respuesta incorrecta. No puedes pasar.")
            return None

    # Marcamos esta celda como visitada
    dp[x][y] = False

    time.sleep(2)
    limpiar_pantalla()
    imprimir_laberinto(laberinto, (x, y))  # Imprimir el laberinto con la posición actual

    # Verificamos las celdas vecinas en las direcciones: derecha, abajo, izquierda, arriba
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy

        # Teletransporte: 3 lleva a 4, y 4 lleva a 3
        if laberinto[x][y] == 3:
            nx, ny = 5, 0  # Teletransporta a (5, 0)
        elif laberinto[x][y] == 4:
            nx, ny = 0, 5  # Teletransporta a (0, 5)

        # Buscamos el siguiente camino recursivamente
        camino = buscar_camino(laberinto, nx, ny, salida, dp)
        if camino:
            return [(x, y)] + camino

    # No hay camino posible desde esta celda
    return None

# Ejecutar la búsqueda del camino
def main():
    imprimir_laberinto(laberinto, entrada)  # Imprimir el laberinto inicial
    camino = encontrar_camino(laberinto, entrada, salida)
    if camino:
        print("¡Camino encontrado!")
        print(camino)
    else:
        print("No se encontró un camino desde la entrada hasta la salida.")

main()
import tkinter as tk
import time

laberinto = [
    [0, 1, 1, 0, 0, 3],  # 3 es teletransporte a 4
    [0, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 111, 0],  # 111 requiere resolver una trivia
    [1, 1, 1, 1, 1, 0],
    [4, 0, 0, 0, 0, 2]  # 4 es teletransporte a 3, 2 es la salida
]

"""laberinto = [
    [0, 1, 0, 0, 0, 3],   # 3 es teletransporte a 4
    [0, 1, 111, 1, 1, 1], # 111 es una trivia
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [4, 1, 1, 1, 1, 2]    # 4 es teletransporte a 3, 2 es la salida
]

laberinto = [
    [0, 1, 0, 0, 0, 3],   # 3 es teletransporte a 4
    [1, 1, 0, 1, 111, 1], # 111 es una trivia
    [0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [4, 1, 0, 1, 1, 2]    # 4 es teletransporte a 3, 2 es la salida
]"""

entrada = (0, 0)
salida = (5, 5)

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title("Laberinto")
        master.geometry("700x500")
        
        # Variable para la respuesta de la trivia
        self.respuesta_var = tk.StringVar()

        # Variable de estado para pausar la búsqueda
        self.en_trivia = False  # Indica si estamos esperando la trivia

        # Label para mostrar mensajes
        self.mensaje_label = tk.Label(self.master, text="")
        self.mensaje_label.place(x=230, y=20)
        
        # Entrada de trivia, oculta por defecto
        self.entrada_trivia = tk.Entry(self.master, textvariable=self.respuesta_var)
        self.boton_enviar_trivia = tk.Button(self.master, text="Enviar", command=self.verificar_respuesta)
        self.respuesta_correcta = False  # Ahora es booleano
        
        # Mostrar el laberinto inicial
        self.mostrar_laberinto(entrada)
        
        # Botón para iniciar la búsqueda del camino
        self.boton_iniciar = tk.Button(self.master, text="Iniciar", command=self.iniciar_busqueda)
        self.boton_iniciar.place(x=310, y=400)
    
    def es_valida(self, x, y):
        return 0 <= x < len(laberinto) and 0 <= y < len(laberinto[0]) and laberinto[x][y] != 1

    def resolver_trivia(self):
        # Mostrar mensaje de trivia
        self.mensaje_label.config(text="¡Has llegado a la celda misteriosa 111! Responde: ¿Cuál es el número primo más pequeño?")
        self.mensaje_label.place(x=100, y=20)

        # Mostrar el cuadro de texto y el botón de envío
        self.entrada_trivia.place(x=280, y=40)
        self.boton_enviar_trivia.place(x=320, y=60)

        # Pausar la búsqueda del camino
        self.en_trivia = True

    def verificar_respuesta(self):
        # Obtener la respuesta del usuario y verificar
        respuesta = self.entrada_trivia.get()

        if respuesta == "2":
            self.mensaje_label.config(text="¡Respuesta correcta! Continuamos.")
            self.respuesta_correcta = True
        else:
            self.mensaje_label.config(text="Respuesta incorrecta. La casilla ahora es una pared.")
            laberinto[3][4] = 1  # Convertir la casilla de trivia en una pared
            self.respuesta_correcta = False
        
        # Ocultar el cuadro de texto y el botón
        self.entrada_trivia.place_forget()
        self.boton_enviar_trivia.place_forget()

        # Continuar el juego desde la posición actual
        self.en_trivia = False
        self.master.after(100, self.reanudar_busqueda)

    def reanudar_busqueda(self):
        # Reanuda la búsqueda después de responder la trivia
        self.buscar_camino(self.x, self.y, salida, self.dp)

    def mostrar_laberinto(self, posicion_actual):
        cell_size = 40
        for i, fila in enumerate(laberinto):
            for j, valor in enumerate(fila):
                if (i, j) == posicion_actual:
                    texto = "0"  # Marca la posición actual con 0
                elif valor == 1:
                    texto = "X"  # Pared
                elif valor == 0:
                    texto = " "  # Camino
                elif valor == 2:
                    texto = "E"  # Salida
                elif valor == 3:
                    texto = "T1"  # Teletransporte a 4
                elif valor == 4:
                    texto = "T2"  # Teletransporte a 3
                elif valor == 111:
                    texto = "Q"  # Pregunta trivia
                label = tk.Label(self.master, text=texto, borderwidth=1, relief="solid", width=4, height=2)
                label.place(x=j * cell_size + 230, y=i * cell_size + 100)

    def buscar_camino(self, x, y, salida, dp):
        if self.en_trivia:
            # Detener la búsqueda si estamos en modo trivia
            return

        if (x, y) == salida:
            self.mensaje_label.config(text="¡Has llegado a la salida!")
            return [(x, y)]

        if not self.es_valida(x, y) or dp[x][y] is not None:
            return None

        if laberinto[x][y] == 111 and not self.respuesta_correcta:
            # Pausar y esperar la trivia
            self.x, self.y, self.dp = x, y, dp  # Guardar estado actual
            self.resolver_trivia()
            return None

        dp[x][y] = False
        
        # Mostrar el laberinto con la posición actual
        self.mostrar_laberinto((x, y))
        self.master.update()  # Actualiza la interfaz para reflejar cambios visuales
        time.sleep(2)  # Pausa de 2 segundos entre movimientos

        # Manejo de teletransporte
        if laberinto[x][y] == 3:
            x, y = 5, 0  # Teletransporte de 3 a 4
        elif laberinto[x][y] == 4:
            x, y = 0, 5  # Teletransporte de 4 a 3

        # Continúa la búsqueda desde la nueva posición
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            camino = self.buscar_camino(nx, ny, salida, dp)
            if camino:
                return [(x, y)] + camino

        return None

    def iniciar_busqueda(self):
        self.dp = [[None for _ in range(len(laberinto[0]))] for _ in range(len(laberinto))]
        self.respuesta_correcta = False  # Resetea la trivia
        self.mensaje_label.config(text="")  # Limpiar mensajes anteriores
        camino = self.buscar_camino(entrada[0], entrada[1], salida, self.dp)
        if camino:
            self.mensaje_label.config(text="¡Camino encontrado!")
        else:
            if not self.en_trivia:  # Solo muestra este mensaje si no está en modo trivia
                self.mensaje_label.config(text="No se encontró un camino.")


# Crear la ventana principal
root = tk.Tk()

# Crear una instancia de la clase Aplicacion
app = Aplicacion(root)

# Ejecutar el bucle principal de la ventana
root.mainloop()

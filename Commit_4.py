import tkinter as tk

laberinto = [
    [0, 1, 1, 0, 0, 3],  # 3 es teletransporte a 4
    [0, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 111, 0],  # 111 requiere resolver una trivia
    [1, 1, 1, 1, 1, 0],
    [4, 0, 0, 0, 0, 2]  # 4 es teletransporte a 3, 2 es la salida
]

entrada = (0, 0)
salida = (5, 5)

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title("Laberinto")
        master.geometry("700x500")
        
        # Variable para la respuesta de la trivia
        self.respuesta_var = tk.StringVar()

        # Label para mostrar mensajes
        self.mensaje_label = tk.Label(self.master, text="")
        self.mensaje_label.place(x=230, y=20)
        
        # Entrada de trivia, oculta por defecto
        self.entrada_trivia = tk.Entry(self.master, textvariable=self.respuesta_var)
        self.boton_enviar_trivia = tk.Button(self.master, text="Enviar", command=self.verificar_respuesta)
        self.respuesta_correcta = None
        
        # Mostrar el laberinto inicial
        self.mostrar_laberinto(entrada)
        
        # Botón para iniciar la búsqueda del camino
        self.boton_iniciar = tk.Button(self.master, text="Iniciar", command=self.iniciar_busqueda)
        self.boton_iniciar.place(x=310, y=400)
    
    def es_valida(self, x, y):
        return 0 <= x < len(laberinto) and 0 <= y < len(laberinto[0]) and laberinto[x][y] != 1

    def resolver_trivia(self):
        self.mensaje_label.config(text="¡Has llegado a la celda misteriosa 111! Responde la pregunta: ¿Cuál es el número primo más pequeño?")
        self.mensaje_label.place(x=100, y=20)

        # Mostrar el cuadro de texto y el botón de envío
        self.entrada_trivia.place(x=280, y=40)
        self.boton_enviar_trivia.place(x=320, y=60)

        # Pausar la búsqueda esperando una respuesta correcta
        self.master.wait_variable(self.respuesta_var)
        
        return self.respuesta_correcta == "2"  # Verifica si la respuesta es correcta

    def verificar_respuesta(self):
        # Obtener la respuesta del usuario y verificar
        respuesta = self.entrada_trivia.get()
        
        if respuesta == "2":
            self.mensaje_label.config(text="¡Respuesta correcta! Puedes continuar.")
            self.respuesta_correcta = "2"
        else:
            self.mensaje_label.config(text="Respuesta incorrecta. Intenta de nuevo.")
            self.respuesta_var.set("")  # Limpiar respuesta si es incorrecta
            return
        
        # Ocultar el cuadro de texto y el botón
        self.entrada_trivia.place_forget()
        self.boton_enviar_trivia.place_forget()
        
        # Continuar el juego
        self.respuesta_var.set(respuesta)

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
        if (x, y) == salida:
            return [(x, y)]

        if not self.es_valida(x, y) or dp[x][y] is not None:
            return None

        if laberinto[x][y] == 111:
            if not self.resolver_trivia():
                return None

        dp[x][y] = False
        
        # Mostrar el laberinto con la posición actual y actualizar la interfaz
        self.mostrar_laberinto((x, y))
        self.master.update()  # Actualiza la interfaz para reflejar cambios visuales

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
        dp = [[None for _ in range(len(laberinto[0]))] for _ in range(len(laberinto))]
        camino = self.buscar_camino(entrada[0], entrada[1], salida, dp)
        if camino:
            self.mensaje_label.config(text="¡Camino encontrado!")
        else:
            self.mensaje_label.config(text="No se encontró un camino.")


# Crear la ventana principal
root = tk.Tk()

# Crear una instancia de la clase Aplicacion
app = Aplicacion(root)

# Ejecutar el bucle principal de la ventana
root.mainloop()

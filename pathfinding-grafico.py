import heapq
import tkinter as tk
import math
import time
from tkinter import messagebox

class Nodo:
    def __init__(self, x, y, costo=0, heuristica=0, padre=None):
        self.x = x
        self.y = y
        self.costo = costo
        self.heuristica = heuristica
        self.padre = padre

    def __lt__(self, otro):
        return (self.costo + self.heuristica) < (otro.costo + otro.heuristica)

def heuristica_euclidiana(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def a_star(inicio, objetivo, mapa):
    filas = len(mapa)
    columnas = len(mapa[0])
    abiertos = []
    cerrados = set()
    inicio_nodo = Nodo(inicio[0], inicio[1], costo=0, heuristica=heuristica_euclidiana(*inicio, *objetivo))
    heapq.heappush(abiertos, inicio_nodo)

    while abiertos:
        nodo_actual = heapq.heappop(abiertos)
        if (nodo_actual.x, nodo_actual.y) == objetivo:
            camino = []
            while nodo_actual:
                camino.append((nodo_actual.x, nodo_actual.y))
                nodo_actual = nodo_actual.padre
            return camino[::-1]
        
        cerrados.add((nodo_actual.x, nodo_actual.y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            x_vecino, y_vecino = nodo_actual.x + dx, nodo_actual.y + dy
            if (0 <= x_vecino < filas and 0 <= y_vecino < columnas and (x_vecino, y_vecino) not in cerrados and mapa[x_vecino][y_vecino] == 0):
                nuevo_costo = nodo_actual.costo + 1
                heuristica = heuristica_euclidiana(x_vecino, y_vecino, *objetivo)
                vecino_nodo = Nodo(x_vecino, y_vecino, costo=nuevo_costo, heuristica=heuristica, padre=nodo_actual)
                heapq.heappush(abiertos, vecino_nodo)
    return None

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding con A*")
        self.canvas_size = 600
        self.cell_size = 6
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        self.mapa = [[0 for _ in range(100)] for _ in range(100)]
        self.inicio = None
        self.objetivo = None
        self.dibujar_mapa()
        self.canvas.bind("<Button-1>", self.seleccionar_celda)
        self.canvas.bind("<B1-Motion>", self.arrastrar_barrera)
        self.boton_inicio = tk.Button(root, text="Seleccionar Inicio", command=self.seleccionar_inicio, bg="black", fg="white")
        self.boton_inicio.pack(side=tk.LEFT)
        self.boton_objetivo = tk.Button(root, text="Seleccionar Objetivo", command=self.seleccionar_objetivo, bg="black", fg="white")
        self.boton_objetivo.pack(side=tk.LEFT)
        self.boton_barrera = tk.Button(root, text="Seleccionar Barrera", command=self.seleccionar_barrera, bg="black", fg="white")
        self.boton_barrera.pack(side=tk.LEFT)
        self.boton_buscar = tk.Button(root, text="Buscar Camino", command=self.buscar_camino, bg="black", fg="white")
        self.boton_buscar.pack(side=tk.LEFT)
        self.boton_limpiar = tk.Button(root, text="Limpiar", command=self.limpiar_mapa, bg="black", fg="white")
        self.boton_limpiar.pack(side=tk.LEFT)
        self.seleccion = None
        self.centrar_ventana()

    def centrar_ventana(self):
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

    def dibujar_mapa(self):
        self.canvas.delete("all")
        for i in range(100):
            for j in range(100):
                color = "white"
                if self.mapa[i][j] == 1:
                    color = "gray"
                self.canvas.create_rectangle(j*self.cell_size, i*self.cell_size, j*self.cell_size+self.cell_size, i*self.cell_size+self.cell_size, fill=color, outline="gray")

    def seleccionar_celda(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if self.seleccion == "inicio":
            if self.inicio:
                self.canvas.create_rectangle(self.inicio[1]*self.cell_size, self.inicio[0]*self.cell_size, self.inicio[1]*self.cell_size+self.cell_size, self.inicio[0]*self.cell_size+self.cell_size, fill="white", outline="gray")
            self.inicio = (y, x)
            self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, x*self.cell_size+self.cell_size, y*self.cell_size+self.cell_size, fill="green", outline="gray")
        elif self.seleccion == "objetivo":
            if self.objetivo:
                self.canvas.create_rectangle(self.objetivo[1]*self.cell_size, self.objetivo[0]*self.cell_size, self.objetivo[1]*self.cell_size+self.cell_size, self.objetivo[0]*self.cell_size+self.cell_size, fill="white", outline="gray")
            self.objetivo = (y, x)
            self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, x*self.cell_size+self.cell_size, y*self.cell_size+self.cell_size, fill="green", outline="gray")
        elif self.seleccion == "barrera":
            self.mapa[y][x] = 1 if self.mapa[y][x] == 0 else 0
            color = "gray" if self.mapa[y][x] == 1 else "white"
            self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, x*self.cell_size+self.cell_size, y*self.cell_size+self.cell_size, fill=color, outline="gray")

    def arrastrar_barrera(self, event):
        if self.seleccion == "barrera":
            x, y = event.x // self.cell_size, event.y // self.cell_size
            if 0 <= x < 100 and 0 <= y < 100:
                self.mapa[y][x] = 1
                self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, x*self.cell_size+self.cell_size, y*self.cell_size+self.cell_size, fill="gray", outline="gray")

    def seleccionar_inicio(self):
        self.seleccion = "inicio"

    def seleccionar_objetivo(self):
        self.seleccion = "objetivo"

    def seleccionar_barrera(self):
        self.seleccion = "barrera"

    def limpiar_mapa(self):
        self.mapa = [[0 for _ in range(100)] for _ in range(100)]
        self.inicio = None
        self.objetivo = None
        self.dibujar_mapa()

    def buscar_camino(self):
        if self.inicio and self.objetivo:
            start_time = time.time()
            camino = a_star(self.inicio, self.objetivo, self.mapa)
            end_time = time.time()
            execution_time = end_time - start_time
            if camino:
                for (y, x) in camino:
                    if self.mapa[y][x] != 1:
                        self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, x*self.cell_size+self.cell_size, y*self.cell_size+self.cell_size, fill="green", outline="gray")
                messagebox.showinfo("Ruta encontrada", f"Ruta: {camino}\nTiempo de ejecución: {execution_time:.4f} segundos")
            else:
                messagebox.showinfo("Ruta no encontrada", "No se encontró camino")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
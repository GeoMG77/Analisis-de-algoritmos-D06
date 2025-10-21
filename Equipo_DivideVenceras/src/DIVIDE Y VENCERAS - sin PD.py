import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Algoritmo Divide y Vencerás ---
def decodificar_divide(cad: str) -> int:
    tam = len(cad)

    def helper(i: int) -> int:
        if i == tam:
            return 1
        if cad[i] == '0':
            return 0
        total = helper(i + 1)
        if i + 1 < tam:
            par = int(cad[i:i+2])
            if 10 <= par <= 26:
                total += helper(i + 2)
        return total

    if tam == 0:
        return 0
    return helper(0)

def num_a_letra(num: str) -> str:
    n = int(num)
    if 1 <= n <= 26:
        return chr(64 + n)
    return "?"

def generar_caminos_str(cad: str) -> list:
    tam = len(cad)
    res_numeros = []

    def back(i: int, camino: list):
        if i == tam:
            res_numeros.append(camino)
            return
        if cad[i] == '0':
            return
        back(i + 1, camino + [cad[i:i+1]])
        if i + 1 < tam:
            par = int(cad[i:i+2])
            if 10 <= par <= 26:
                back(i + 2, camino + [cad[i:i+2]])

    back(0, [])
    res_cadenas = []
    if not res_numeros:
        res_cadenas.append("No hay formas posibles de decodificar esta cadena.")
    else:
        res_cadenas.append("Formas posibles:")
        for camino in res_numeros:
            letras = "".join(num_a_letra(x) for x in camino)
            res_cadenas.append(f"  {'|'.join(camino)} -> {letras}")
    return res_cadenas

# --- Interfaz Gráfica ---
class DecodificadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Decodificador de Mensajes (Divide y Vencerás)")
        self.root.geometry("600x650")
        self.datos_n = []
        self.datos_tiempos = []
        self.crear_widgets()
        self.crear_grafica()

    def crear_widgets(self):
        frame_top = ttk.Frame(self.root, padding=10)
        frame_top.pack(fill='x')

        ttk.Label(frame_top, text="Ingresa el mensaje numérico:").pack(fill='x')
        self.entry_cadena = ttk.Entry(frame_top, width=60)
        self.entry_cadena.pack(fill='x', pady=5)

        self.btn_analizar = ttk.Button(frame_top, text="Analizar", command=self.iniciar_analisis)
        self.btn_analizar.pack(pady=5)

        self.txt_resultados = scrolledtext.ScrolledText(frame_top, height=10, width=70, wrap=tk.WORD)
        self.txt_resultados.pack(fill='both', expand=True, pady=5)

    def crear_grafica(self):
        frame_graph = ttk.Frame(self.root, padding=10)
        frame_graph.pack(fill='both', expand=True)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Rendimiento en Tiempo Real (Divide y Vencerás)")
        self.ax.set_xlabel("Longitud de la cadena (n)")
        self.ax.set_ylabel("Tiempo (segundos) - Escala Logarítmica")
        self.ax.grid(True)
        self.ax.set_yscale('log')
        self.line, = self.ax.plot(self.datos_n, self.datos_tiempos, 'bo')

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def iniciar_analisis(self):
        cad = self.entry_cadena.get()
        self.txt_resultados.delete('1.0', tk.END)
        if not cad.isdigit():
            self.txt_resultados.insert(tk.END, "Error: Solo se permiten números.")
            return
        if len(cad) == 0:
            self.txt_resultados.insert(tk.END, "Error: Cadena vacía.")
            return
        self.btn_analizar.config(state=tk.DISABLED)
        self.txt_resultados.insert(tk.END, f"Analizando '{cad}' (n={len(cad)})...\nEsto puede tardar si n > 25.\n")
        self.root.update_idletasks()
        threading.Thread(target=self.hilo_calcular, args=(cad,), daemon=True).start()

    def hilo_calcular(self, cad: str):
        try:
            n = len(cad)
            start_time = time.perf_counter()
            total = decodificar_divide(cad)
            end_time = time.perf_counter()
            duracion = end_time - start_time
            caminos_str = generar_caminos_str(cad)
            self.root.after(0, self.actualizar_gui_post_calculo, n, duracion, total, caminos_str)
        except Exception as e:
            self.root.after(0, self.reportar_error, str(e))

    def actualizar_gui_post_calculo(self, n: int, duracion: float, total: int, caminos_str: list):
        self.txt_resultados.insert(tk.END, "\n".join(caminos_str))
        self.txt_resultados.insert(tk.END, f"\n\nTotal de formas posibles: {total}")
        self.txt_resultados.insert(tk.END, f"\n\n--- Tiempo de ejecución: {duracion:.8f} segundos ---")
        self.datos_n.append(n)
        self.datos_tiempos.append(duracion if duracion > 0 else 1e-9)
        self.line.set_xdata(self.datos_n)
        self.line.set_ydata(self.datos_tiempos)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.tight_layout()
        self.canvas.draw()
        self.btn_analizar.config(state=tk.NORMAL)

    def reportar_error(self, error_msg: str):
        self.txt_resultados.insert(tk.END, f"\n\nERROR: {error_msg}")
        self.btn_analizar.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DecodificadorApp(root)
    root.mainloop()

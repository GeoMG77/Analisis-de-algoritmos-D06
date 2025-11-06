import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import heapq
import os

# ---- NODO DEL ÁRBOL DE HUFFMAN ----
class NodoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.izq = None
        self.der = None

    # Para usar en la cola de prioridad
    def __lt__(self, otro):
        return self.freq < otro.freq


# ---- FUNCIONES DEL ALGORITMO DE HUFFMAN ----
def calcular_frecuencias(texto):
    frecuencias = {}
    for caracter in texto:
        frecuencias[caracter] = frecuencias.get(caracter, 0) + 1
    return frecuencias


def construir_arbol(frecuencias):
    heap = [NodoHuffman(c, f) for c, f in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        izq = heapq.heappop(heap)
        der = heapq.heappop(heap)
        nodo_padre = NodoHuffman(None, izq.freq + der.freq)
        nodo_padre.izq = izq
        nodo_padre.der = der
        heapq.heappush(heap, nodo_padre)

    return heap[0] if heap else None


def generar_codigos(nodo, codigo="", codigos={}):
    if nodo is None:
        return
    if nodo.char is not None:
        codigos[nodo.char] = codigo
    generar_codigos(nodo.izq, codigo + "0", codigos)
    generar_codigos(nodo.der, codigo + "1", codigos)
    return codigos


def codificar_texto(texto, codigos):
    return ''.join(codigos[c] for c in texto)


def decodificar_texto(codificado, arbol):
    resultado = ""
    nodo_actual = arbol
    for bit in codificado:
        nodo_actual = nodo_actual.izq if bit == "0" else nodo_actual.der
        if nodo_actual.char is not None:
            resultado += nodo_actual.char
            nodo_actual = arbol
    return resultado


# ---- INTERFAZ GRÁFICA ----
class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor Huffman - Técnica Voraz")
        self.root.geometry("700x600")
        self.root.config(bg="#ECECEC")

        self.archivo = ""
        self.texto_original = ""
        self.codificado = ""
        self.codigos = {}
        self.arbol = None

        # ---- INTERFAZ ----
        tk.Label(root, text="Algoritmo de Huffman (Compresión de texto)",
                 font=("Arial", 16, "bold"), bg="#ECECEC").pack(pady=10)

        tk.Button(root, text="Seleccionar archivo .txt", command=self.cargar_archivo,
                  font=("Arial", 12), bg="#D0E6A5").pack(pady=5)

        tk.Button(root, text="Ejecutar Compresión", command=self.ejecutar_huffman,
                  font=("Arial", 12), bg="#FFD97D").pack(pady=5)

        tk.Button(root, text="Decodificar texto", command=self.decodificar,
                  font=("Arial", 12), bg="#A0CED9").pack(pady=5)

        self.resultado = scrolledtext.ScrolledText(root, width=80, height=25, font=("Courier", 10))
        self.resultado.pack(pady=10)

    # ---- FUNCIONES GUI ----
    def cargar_archivo(self):
        self.archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.archivo:
            with open(self.archivo, "r", encoding="utf-8", errors="ignore") as f:
                self.texto_original = f.read()
            messagebox.showinfo("Archivo cargado", f"Se cargó el archivo:\n{os.path.basename(self.archivo)}")

    def ejecutar_huffman(self):
        if not self.texto_original:
            messagebox.showwarning("Advertencia", "Primero carga un archivo .txt")
            return

        frecuencias = calcular_frecuencias(self.texto_original)
        self.arbol = construir_arbol(frecuencias)
        self.codigos = generar_codigos(self.arbol)
        self.codificado = codificar_texto(self.texto_original, self.codigos)

        # Guardar archivo comprimido
        archivo_cod = self.archivo.replace(".txt", "_codificado.txt")
        with open(archivo_cod, "w") as f:
            f.write(self.codificado)

        tam_original = os.path.getsize(self.archivo)
        tam_codificado = os.path.getsize(archivo_cod)
        compresion = 100 - (tam_codificado / tam_original * 100)

        salida = "Resultados de Compresión de Huffman\n"
        salida += f"\nArchivo original: {os.path.basename(self.archivo)}"
        salida += f"\nTamaño original: {tam_original} bytes"
        salida += f"\nTamaño codificado: {tam_codificado} bytes"
        salida += f"\nCompresión lograda: {compresion:.2f}%"
        salida += "\n\nCódigos Huffman generados:\n"
        for c, code in sorted(self.codigos.items(), key=lambda x: x[0]):
            salida += f"{repr(c)} : {code}\n"

        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(tk.END, salida)

    def decodificar(self):
        if not self.codificado or not self.arbol:
            messagebox.showwarning("Advertencia", "Primero ejecuta la compresión")
            return
        decod = decodificar_texto(self.codificado, self.arbol)
        self.resultado.insert(tk.END, "\n\n Texto decodificado (primeros 300 caracteres):\n")
        self.resultado.insert(tk.END, decod[:300] + "...")


# ---- EJECUCIÓN ----
if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()

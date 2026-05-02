import os
import heapq
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter


class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otroNodo):
        return self.frecuencia < otroNodo.frecuencia


def construirArbol(frecuencias):
    colaPrioridad = [NodoHuffman(car, freq)
                     for car, freq in frecuencias.items()]
    heapq.heapify(colaPrioridad)

    while len(colaPrioridad) > 1:
        nodoIzq = heapq.heappop(colaPrioridad)
        nodoDer = heapq.heappop(colaPrioridad)
        nodoPadre = NodoHuffman(None, nodoIzq.frecuencia + nodoDer.frecuencia)
        nodoPadre.izquierda = nodoIzq
        nodoPadre.derecha = nodoDer
        heapq.heappush(colaPrioridad, nodoPadre)

    return colaPrioridad[0]


def generarCodigos(nodo, codigoActual="", codigos={}):
    if nodo is None:
        return

    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigoActual

    generarCodigos(nodo.izquierda, codigoActual + "0", codigos)
    generarCodigos(nodo.derecha, codigoActual + "1", codigos)

    return codigos


def codificarTexto(texto, codigos):
    return "".join(codigos[car] for car in texto)


def decodificarTexto(textoCodificado, raiz):
    resultado = ""
    nodoActual = raiz

    for bit in textoCodificado:
        nodoActual = nodoActual.izquierda if bit == '0' else nodoActual.derecha

        if nodoActual.caracter is not None:
            resultado += nodoActual.caracter
            nodoActual = raiz

    return resultado


def calcularFrecuencias(texto):
    return Counter(texto)


class InterfazHuffman:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Compresión Huffman")
        self.rutaArchivo = ""

        self.botonCargar = tk.Button(
            ventana, text="Cargar Archivo", command=self.cargarArchivo)
        self.botonCargar.pack(pady=10)

        self.botonProcesar = tk.Button(
            ventana, text="Procesar Huffman", command=self.procesar)
        self.botonProcesar.pack(pady=10)

        self.textoResultado = tk.Text(ventana, height=20, width=80)
        self.textoResultado.pack(pady=10)

    def cargarArchivo(self):
        self.rutaArchivo = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")])
        if self.rutaArchivo:
            messagebox.showinfo("Archivo", "Archivo cargado correctamente")

    def procesar(self):
        if not self.rutaArchivo:
            messagebox.showwarning("Error", "Cargue un archivo primero")
            return

        with open(self.rutaArchivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

        frecuencias = calcularFrecuencias(contenido)
        raiz = construirArbol(frecuencias)
        codigos = generarCodigos(raiz)

        textoCodificado = codificarTexto(contenido, codigos)
        textoDecodificado = decodificarTexto(textoCodificado, raiz)

        tamañoOriginal = len(contenido) * 8
        tamañoComprimido = len(textoCodificado)

        eficiencia = 100 * (1 - (tamañoComprimido / tamañoOriginal))

        self.textoResultado.delete(1.0, tk.END)
        self.textoResultado.insert(
            tk.END, "Frecuencias:\n" + str(frecuencias) + "\n\n")
        self.textoResultado.insert(
            tk.END, "Codigos:\n" + str(codigos) + "\n\n")
        self.textoResultado.insert(
            tk.END, f"Tamaño original (bits): {tamañoOriginal}\n")
        self.textoResultado.insert(
            tk.END, f"Tamaño comprimido (bits): {tamañoComprimido}\n")
        self.textoResultado.insert(
            tk.END, f"Eficiencia: {eficiencia:.2f}%\n\n")

        if contenido == textoDecodificado:
            self.textoResultado.insert(tk.END, "Decodificación correcta")
        else:
            self.textoResultado.insert(tk.END, "Error en decodificación")


if __name__ == "__main__":
    ventanaPrincipal = tk.Tk()
    app = InterfazHuffman(ventanaPrincipal)
    ventanaPrincipal.mainloop()

import tkinter as tk
import matplotlib.pyplot as plt
from math import atan2  # for computing polar angle
import pandas as pd  # leer CSV
import math  # para calcular distancia

puntos_actuales = []  # para almacenar puntos leídos desde CSV

# Leer puntos desde CSV
# se cambia el nombre de "puntos.csv" coordenadas_768_puntos_0_1000.csv

def leer_puntos():
    global puntos_actuales

    df = pd.read_csv("coordenadas_768_puntos_0_1000.csv") 
    print(df.columns)
    puntos_actuales = df[['x', 'y']].values.tolist()

    hull = graham_scan(puntos_actuales)
    scatter_plot(puntos_actuales, hull)


# FUNCIONES GRAHAM SCAN
def polar_angle(p0, p1=None):
    if p1 is None:
        p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return atan2(y_span, x_span)


def distance(p0, p1=None):
    if p1 is None:
        p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return y_span**2 + x_span**2


def det(p1, p2, p3):
    return ((p2[0] - p1[0]) * (p3[1] - p1[1]) -
            (p2[1] - p1[1]) * (p3[0] - p1[0]))


def graham_scan(points):
    global anchor

    if len(points) < 3:
        return points

    # Encontrar punto más bajo
    anchor = min(points, key=lambda p: (p[1], p[0]))

    sorted_pts = sorted(points, key=lambda p: (polar_angle(p), -distance(p)))
    sorted_pts.remove(anchor)

    hull = [anchor, sorted_pts[0]]

    for s in sorted_pts[1:]:
        while len(hull) > 1 and det(hull[-2], hull[-1], s) <= 0:
            hull.pop()
        hull.append(s)

    return hull
    """
    Esta funcion del codigo es equivalente a la que se pide aqui 

    def orientacion(a: Point, b: Point, c: Point) -> float:
    TODO:
    Regresa el valor del producto cruz (cross product).

    Pista :
    cross = (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

    Interpretación:
    - cross > 0  : giro antihorario (CCW)
    - cross < 0  : giro horario (CW)
    - cross == 0 : colineales

    raise NotImplementedError("Completa la función orientacion(a, b, c)")

    """

def scatter_plot(points, hull):
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]

    plt.scatter(x_vals, y_vals)

    if hull:
        for i in range(len(hull)):
            p1 = hull[i]
            p2 = hull[(i + 1) % len(hull)]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r')

    plt.title("Convex Hull - Graham Scan")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


# calcular puntos más cercanos
def mejor_par():
    global puntos_actuales

    if puntos_actuales:
        puntos = puntos_actuales
    else:
        puntos = obtener_puntos()
    """ Si ya se han leído puntos desde el CSV, los usamos. De lo contrario, obtenemos los puntos de las entradas de la GUI.
    Esto permite que el usuario pueda calcular el mejor par tanto para los puntos ingresados manualmente como 
    para los puntos cargados desde el CSV. """

    distancia_min = float("inf")
    mejor_par = None

    n = len(puntos)

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = puntos[i]
            x2, y2 = puntos[j]

            distancia = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

            if distancia < distancia_min:
                distancia_min = distancia
                mejor_par = (puntos[i], puntos[j])

    if mejor_par:
        label_resultado.config(
            text=f"Distancia mínima: {distancia_min:.4f}\nEntre {mejor_par[0]} y {mejor_par[1]}"
        )

    return mejor_par


# FUNCIONES GUI
def obtener_puntos():
    puntos = []

    for ex, ey in entradas:
        if ex.get() != "" and ey.get() != "":
            try:
                x = float(ex.get())
                y = float(ey.get())
                puntos.append((x, y))
            except ValueError:
                pass

    return puntos


def ejecutar_graham():
    puntos = obtener_puntos()

    if len(puntos) < 3:
        label_resultado.config(text="Se necesitan al menos 3 puntos")
        return
    hull = graham_scan(puntos)
    label_resultado.config(text=f"Convex Hull:\n{hull}")
    # Esta función se encarga de mostrar la gráfica con los puntos y el convex hull. Se llama después de calcular el convex hull para visualizar los resultados.
    scatter_plot(puntos, hull)

    """
    Esta funcion del codigo es equivalente a la que se pide aqui 
    def convex_hull(puntos: List[Point]) -> List[Point]:
    TODO:

    Idea general:
    1) Empieza en el punto más a la izquierda.
    2) En cada paso, elige el siguiente punto q tal que para cualquier otro punto r,
       el giro desde p hacia q sea el “más externo”.
    3) Repite hasta regresar al punto inicial.

    Nota:
    - Maneja colineales: si varios puntos quedan en la misma línea,
      quédate con el más lejano para que la envolvente quede “por fuera”.
    if len(puntos) < 3:
        return puntos[:]  # no hay polígono

    hull: List[Point] = []
    start_idx = punto_mas_izquierdo(puntos)
    p_idx = start_idx

    while True:
        hull.append(puntos[p_idx])
        q_idx = (p_idx + 1) % len(puntos)

        for r_idx in range(len(puntos)):
            if r_idx == p_idx:
                continue

            # TODO:
            # 1) Calcula o = orientacion(p, q, r)
            # 2) Si r es “más externo” que q, entonces q = r
            # 3) Si son colineales, elige el más lejano a p
            #
            # Sugerencia de convención:
            # - Si tu orientacion devuelve >0 para CCW,
            #   normalmente querrás elegir el punto con giro CCW “más externo”.
            # Ajusta la condición según tu convención.
            pass

        p_idx = q_idx
        if p_idx == start_idx:
            break

    return hull
"""

# CREAR VENTANA
ventana = tk.Tk()
ventana.title("Convex Hull - Graham Scan")
ventana.geometry("400x500")

tk.Label(ventana, text="Ingresa 5 puntos (x,y)").pack(pady=10)

entradas = []

for i in range(5):
    frame = tk.Frame(ventana)
    frame.pack(pady=5)

    tk.Label(frame, text=f"x{i+1}=").pack(side="left")
    entrada_x = tk.Entry(frame, width=10)
    entrada_x.pack(side="left", padx=5)

    tk.Label(frame, text=f"y{i+1}=").pack(side="left")
    entrada_y = tk.Entry(frame, width=10)
    entrada_y.pack(side="left")

    entradas.append((entrada_x, entrada_y))


boton = tk.Button(ventana, text="Calcular Convex Hull",
                  command=ejecutar_graham)
boton.pack(pady=15)

boton2 = tk.Button(ventana, text="Calcular mejor par", command=mejor_par)
boton2.pack(pady=15)

boton3 = tk.Button(ventana, text="Cargar puntos desde CSV",
                   command=leer_puntos)
boton3.pack(pady=15)

label_resultado = tk.Label(ventana, text="", fg="blue")
label_resultado.pack(pady=10)

ventana.mainloop()

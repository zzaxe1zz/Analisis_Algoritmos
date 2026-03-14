import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.collections import LineCollection
from sklearn.neighbors import kneighbors_graph
import umap

# 1. CARGA Y PREPROCESAMIENTO DE DATOS
print("Cargando el archivo fashion-mnist_test.csv...")
datos_ropa = pd.read_csv('fashion-mnist_test.csv')

# Separación de etiquetas y normalización de píxeles
etiquetas_ropa = datos_ropa['label'].values
pixeles_normalizados = datos_ropa.drop('label', axis=1).values / 255.0

nombres_categorias = ['Camiseta/Top', 'Pantalón', 'Pullover', 'Vestido', 'Abrigo',
                      'Sandalia', 'Camisa', 'Zapatilla', 'Bolso', 'Botín']

# 2. REDUCCIÓN DE DIMENSIONALIDAD (PROYECCIÓN UMAP)
print("Ejecutando algoritmo UMAP para reducción de dimensiones...")
proyector_espacial = umap.UMAP(n_neighbors=15, min_dist=0.1,
                               n_components=2, random_state=42)
coordenadas_2d = proyector_espacial.fit_transform(pixeles_normalizados)

# 3. GENERACIÓN DE LA ESTRUCTURA DE CONEXIONES (RAMAS)
print("Calculando grafo de vecindad para las ramas...")
# Generamos las conexiones entre puntos cercanos
grafo_vecinos = kneighbors_graph(pixeles_normalizados, n_neighbors=2,
                                 mode='connectivity', include_self=False)

# 4. CONFIGURACIÓN DEL LIENZO VISUAL
plt.ion()
figura, eje_visual = plt.subplots(figsize=(12, 10))
figura.canvas.manager.set_window_title('Explorador de Clusters Fashion-MNIST')

# Cambio de fondo a BLANCO como solicitaste
figura.patch.set_facecolor('white')
eje_visual.set_facecolor('white')

# Dibujo de las Ramas en NEGRO
print("Trazando ramas de conexión...")
indices_filas, indices_cols = grafo_vecinos.nonzero()
segmentos_lineas = np.stack(
    [coordenadas_2d[indices_filas], coordenadas_2d[indices_cols]], axis=1)

coleccion_ramas = LineCollection(segmentos_lineas, colors="black",
                                 linewidths=0.15, alpha=0.3, zorder=1)
eje_visual.add_collection(coleccion_ramas)

# Dibujo de los Puntos (Nodos)
puntos_dispersos = eje_visual.scatter(coordenadas_2d[:, 0], coordenadas_2d[:, 1],
                                      c=etiquetas_ropa, cmap='tab10', s=3,
                                      alpha=0.7, edgecolors='none', zorder=2, picker=True)

# 5. ELEMENTOS INTERACTIVOS (HOVER)
# Caja para mostrar la miniatura de la prenda
caja_imagen = OffsetImage(np.zeros((28, 28)), zoom=3.5, cmap='gray')
anotacion_img = AnnotationBbox(caja_imagen, (0, 0), xybox=(50, 50), xycoords='data',
                               boxcoords="offset points", pad=0.2,
                               arrowprops=dict(arrowstyle="->", color='black'),
                               bboxprops=dict(edgecolor='black', linewidth=1))
anotacion_img.set_visible(False)
eje_visual.add_artist(anotacion_img)

# Etiqueta de texto descriptiva
etiqueta_texto = eje_visual.annotate("", xy=(0, 0), xytext=(50, 110), textcoords="offset points",
                                     color="black", fontsize=9, fontweight='bold',
                                     bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="black", alpha=0.8))
etiqueta_texto.set_visible(False)


def actualizar_cursor(event):
    if event.inaxes == eje_visual:
        contenido, indices = puntos_dispersos.contains(event)
        if contenido:
            idx_punto = indices['ind'][0]
            ubicacion = coordenadas_2d[idx_punto]

            anotacion_img.xy = ubicacion
            etiqueta_texto.xy = ubicacion

            # Actualizar contenido visual
            matriz_prenda = pixeles_normalizados[idx_punto].reshape(28, 28)
            caja_imagen.set_data(matriz_prenda)

            nombre_clase = nombres_categorias[etiquetas_ropa[idx_punto]]
            etiqueta_texto.set_text(
                f"ID: {etiquetas_ropa[idx_punto]} | {nombre_clase}")

            anotacion_img.set_visible(True)
            etiqueta_texto.set_visible(True)
            figura.canvas.draw_idle()
        else:
            if anotacion_img.get_visible():
                anotacion_img.set_visible(False)
                etiqueta_texto.set_visible(False)
                figura.canvas.draw_idle()


figura.canvas.mpl_connect('motion_notify_event', actualizar_cursor)

# Limpieza Estética Final
eje_visual.set_xticks([])
eje_visual.set_yticks([])
for borde in eje_visual.spines.values():
    borde.set_visible(False)

plt.title("Visualización UMAP: Fashion-MNIST (10k Registros)",
          color='black', size=15, pad=20)

print("Proceso completado. Mostrando ventana interactiva...")
plt.ioff()
plt.show()


# 1. CARGA Y PREPROCESAMIENTO DE DATOS
print("Cargando el archivo fashion-mnist_test.csv...")
datos_ropa = pd.read_csv('fashion-mnist_test.csv')

# Separación de etiquetas y normalización de píxeles
etiquetas_ropa = datos_ropa['label'].values
pixeles_normalizados = datos_ropa.drop('label', axis=1).values / 255.0

nombres_categorias = ['Camiseta/Top', 'Pantalón', 'Pullover', 'Vestido', 'Abrigo',
                      'Sandalia', 'Camisa', 'Zapatilla', 'Bolso', 'Botín']

# 2. REDUCCIÓN DE DIMENSIONALIDAD (PROYECCIÓN UMAP)
print("Ejecutando algoritmo UMAP para reducción de dimensiones...")
proyector_espacial = umap.UMAP(n_neighbors=15, min_dist=0.1,
                               n_components=2, random_state=42)
coordenadas_2d = proyector_espacial.fit_transform(pixeles_normalizados)

# 3. GENERACIÓN DE LA ESTRUCTURA DE CONEXIONES (RAMAS)
print("Calculando grafo de vecindad para las ramas...")
# Generamos las conexiones entre puntos cercanos
grafo_vecinos = kneighbors_graph(pixeles_normalizados, n_neighbors=2,
                                 mode='connectivity', include_self=False)

# 4. CONFIGURACIÓN DEL LIENZO VISUAL
plt.ion()
figura, eje_visual = plt.subplots(figsize=(12, 10))
figura.canvas.manager.set_window_title('Explorador de Clusters Fashion-MNIST')

# Cambio de fondo a BLANCO como solicitaste
figura.patch.set_facecolor('white')
eje_visual.set_facecolor('white')

# Dibujo de las Ramas en NEGRO
print("Trazando ramas de conexión...")
indices_filas, indices_cols = grafo_vecinos.nonzero()
segmentos_lineas = np.stack(
    [coordenadas_2d[indices_filas], coordenadas_2d[indices_cols]], axis=1)

coleccion_ramas = LineCollection(segmentos_lineas, colors="black",
                                 linewidths=0.15, alpha=0.3, zorder=1)
eje_visual.add_collection(coleccion_ramas)

# Dibujo de los Puntos (Nodos)
puntos_dispersos = eje_visual.scatter(coordenadas_2d[:, 0], coordenadas_2d[:, 1],
                                      c=etiquetas_ropa, cmap='tab10', s=3,
                                      alpha=0.7, edgecolors='none', zorder=2, picker=True)

# 5. ELEMENTOS INTERACTIVOS (HOVER)
# Caja para mostrar la miniatura de la prenda
caja_imagen = OffsetImage(np.zeros((28, 28)), zoom=3.5, cmap='gray')
anotacion_img = AnnotationBbox(caja_imagen, (0, 0), xybox=(50, 50), xycoords='data',
                               boxcoords="offset points", pad=0.2,
                               arrowprops=dict(arrowstyle="->", color='black'),
                               bboxprops=dict(edgecolor='black', linewidth=1))
anotacion_img.set_visible(False)
eje_visual.add_artist(anotacion_img)

# Etiqueta de texto descriptiva
etiqueta_texto = eje_visual.annotate("", xy=(0, 0), xytext=(50, 110), textcoords="offset points",
                                     color="black", fontsize=9, fontweight='bold',
                                     bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="black", alpha=0.8))
etiqueta_texto.set_visible(False)


def actualizar_cursor(event):
    if event.inaxes == eje_visual:
        contenido, indices = puntos_dispersos.contains(event)
        if contenido:
            idx_punto = indices['ind'][0]
            ubicacion = coordenadas_2d[idx_punto]

            anotacion_img.xy = ubicacion
            etiqueta_texto.xy = ubicacion

            # Actualizar contenido visual
            matriz_prenda = pixeles_normalizados[idx_punto].reshape(28, 28)
            caja_imagen.set_data(matriz_prenda)

            nombre_clase = nombres_categorias[etiquetas_ropa[idx_punto]]
            etiqueta_texto.set_text(
                f"ID: {etiquetas_ropa[idx_punto]} | {nombre_clase}")

            anotacion_img.set_visible(True)
            etiqueta_texto.set_visible(True)
            figura.canvas.draw_idle()
        else:
            if anotacion_img.get_visible():
                anotacion_img.set_visible(False)
                etiqueta_texto.set_visible(False)
                figura.canvas.draw_idle()


figura.canvas.mpl_connect('motion_notify_event', actualizar_cursor)

# Limpieza Estética Final
eje_visual.set_xticks([])
eje_visual.set_yticks([])
for borde in eje_visual.spines.values():
    borde.set_visible(False)

plt.title("Visualización UMAP: Fashion-MNIST (10k Registros)",
          color='black', size=15, pad=20)

print("Proceso completado. Mostrando ventana interactiva...")
plt.ioff()
plt.show()

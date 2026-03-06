import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.collections import LineCollection
from sklearn.neighbors import kneighbors_graph
import umap

# 1. CARGA DE DATOS
print("Leyendo fashion-mnist_test.csv...")
df = pd.read_csv('fashion-mnist_test.csv')

y = df['label'].values
X = df.drop('label', axis=1).values / 255.0

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# 2. REDUCCIÓN DE DIMENSIONALIDAD CON UMAP
print("Calculando UMAP (esto puede tardar 1-2 minutos para 10k puntos)...")
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1,
                    n_components=2, random_state=42)
pos = reducer.fit_transform(X)

# 3. CREACIÓN DE LAS RAMAS (Grafo KNN)
print("Generando estructura de conexiones (ramas)...")
# n_neighbors=2 crea las conexiones tipo "hilo" para el efecto de ramas al hacer zoom
A = kneighbors_graph(X, n_neighbors=2, mode='connectivity', include_self=False)

# 4. CONFIGURACIÓN DE LA VENTANA EMERGENTE
# Forzamos a que sea una ventana interactiva independiente
plt.ion()
fig, ax = plt.subplots(figsize=(12, 10))
fig.canvas.manager.set_window_title('Fashion MNIST UMAP Explorer')
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Dibujar las Ramas (Líneas)
print("Dibujando ramas...")
row_idx, col_idx = A.nonzero()
lines = np.stack([pos[row_idx], pos[col_idx]], axis=1)
lc = LineCollection(lines, colors="#FFFFFF",
                    linewidths=0.2, alpha=0.5, zorder=1)
ax.add_collection(lc)

# Dibujar los Puntos (Nodos) con colores por categoría
print("Dibujando puntos...")
scatter = ax.scatter(pos[:, 0], pos[:, 1], c=y, cmap='Spectral', s=2,
                     alpha=0.8, edgecolors='none', zorder=2, picker=True)

# 5. LÓGICA DEL HOVER (Imagen emergente)
image_box = OffsetImage(np.zeros((28, 28)), zoom=4, cmap='gray')
ab = AnnotationBbox(image_box, (0, 0), xybox=(60, 60), xycoords='data',
                    boxcoords="offset points", pad=0.3,
                    arrowprops=dict(arrowstyle="->", color='white'),
                    bboxprops=dict(edgecolor='white', linewidth=1.5))
ab.set_visible(False)
ax.add_artist(ab)

text_ann = ax.annotate("", xy=(0, 0), xytext=(60, 125), textcoords="offset points",
                       color="white", fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.5", fc="#222222", ec="white", alpha=0.9))
text_ann.set_visible(False)


def on_mouse_move(event):
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            idx = ind['ind'][0]
            point_pos = pos[idx]

            ab.xy = point_pos
            text_ann.xy = point_pos

            # Actualizar imagen y texto
            img = X[idx].reshape(28, 28)
            image_box.set_data(img)
            text_ann.set_text(f" Clase {y[idx]}: {class_names[y[idx]]} ")

            ab.set_visible(True)
            text_ann.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if ab.get_visible():
                ab.set_visible(False)
                text_ann.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

# Limpieza estética de la ventana
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.title("Fashion MNIST - Visualización UMAP (10,000 registros)",
          color='white', size=14)
print("Ventana emergente abierta.")
plt.ioff()
plt.show()

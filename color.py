from skimage import io
from sklearn.cluster import KMeans
import webcolors

# Cargar la imagen
imagen = io.imread('recortada.jpg')

# Obtener las dimensiones de la imagen
alto, ancho, _ = imagen.shape

# Redimensionar la imagen para facilitar el procesamiento
imagen_redimensionada = imagen.reshape(alto * ancho, 3)

# Aplicar el algoritmo de K-Means para encontrar los colores dominantes
kmeans = KMeans(n_clusters=5, n_init=10)  # Establecer n_init en 10
kmeans.fit(imagen_redimensionada)

# Obtener los colores dominantes
colores_dominantes = kmeans.cluster_centers_

# Convertir los valores de los colores a enteros
colores_dominantes = colores_dominantes.round().astype(int)

# Imprimir los colores RGB dominantes
for color in colores_dominantes:
    print("Color RGB:", color)
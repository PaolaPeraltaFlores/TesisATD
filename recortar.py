import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('segmentar8.jpg')

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar un umbral para obtener una imagen binaria del contorno azul
umbral_inf = np.array([100, 0, 0])  # BGR - límite inferior para el color azul
umbral_sup = np.array([255, 50, 50])  # BGR - límite superior para el color azul
mascara_azul = cv2.inRange(imagen, umbral_inf, umbral_sup)

# Encontrar los contornos en la imagen binaria
contornos, _ = cv2.findContours(mascara_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Crear una máscara en blanco del tamaño de la imagen original
mascara_recorte = np.zeros_like(imagen_gris)

# Dibujar todos los contornos en la máscara
cv2.drawContours(mascara_recorte, contornos, -1, (255), thickness=cv2.FILLED)

# Aplicar la máscara al contorno original para recortar
imagen_recortada = cv2.bitwise_and(imagen, imagen, mask=mascara_recorte)

# Convertir los píxeles azules en blanco en la imagen recortada
imagen_recortada[np.where(mascara_azul == 255)] = [255, 255, 255]

# Crear una imagen en blanco del mismo tamaño que la imagen original
imagen_fondo_blanco = np.ones_like(imagen) * 255

# Aplicar la máscara inversa al fondo blanco para el contorno azul
mascara_contorno_azul = cv2.bitwise_not(mascara_recorte)
imagen_fondo_blanco = cv2.bitwise_and(imagen_fondo_blanco, imagen_fondo_blanco, mask=mascara_contorno_azul)

# Combinar la imagen recortada y el fondo blanco
imagen_recortada_final = cv2.add(imagen_recortada, imagen_fondo_blanco)

# Guardar la imagen resultante
cv2.imwrite('recortar8.jpg', imagen_recortada_final)

# Mostrar la imagen original y la imagen recortada
#cv2.imshow('Imagen Original', imagen)
#cv2.imshow('Imagen Recortada', imagen_recortada_final)
#cv2.waitKey(1)
#cv2.destroyAllWindows()

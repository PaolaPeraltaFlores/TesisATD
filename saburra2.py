import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('recorsab.jpg')

# Convertir la imagen a escala de grises
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Umbralizar la imagen para obtener los píxeles blancos
_, umbralizada = cv2.threshold(grises, 200, 255, cv2.THRESH_BINARY)

# Encontrar los contornos de los píxeles blancos
contornos, _ = cv2.findContours(umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos encontrados en la imagen original
cv2.drawContours(imagen, contornos, -1, (0, 255, 0), 2)

# Mostrar la imagen resultante
cv2.imshow('Resultado', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()

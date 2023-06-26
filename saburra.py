import cv2
import numpy as np

def encontrar_pixeles_fondo_blanco(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Binarizar la imagen usando un umbral
    _, imagen_binaria = cv2.threshold(imagen_gris, 200, 255, cv2.THRESH_BINARY)

    # Encontrar los contornos de los objetos en la imagen binaria
    contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar los píxeles de fondo blanco
    pixeles_fondo_blanco = []
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 100:  # Descartar contornos muy pequeños
            x, y, w, h = cv2.boundingRect(contorno)
            pixeles_fondo_blanco.extend([(x, y), (x + w, y + h)])

    return pixeles_fondo_blanco

# Cargar la imagen
imagen = cv2.imread('recortar1.jpg')

# Encontrar los píxeles de fondo blanco
pixeles = encontrar_pixeles_fondo_blanco(imagen)

# Imprimir los resultados
print("Píxeles de fondo blanco encontrados:")
for pixel in pixeles:
    print(pixel)

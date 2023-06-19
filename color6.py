import cv2
import numpy as np

def reconocer_color(imagen):
    # Leer la imagen
    imagen = cv2.imread(imagen)

    # Convertir la imagen a HSV
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Definir los umbrales de color para rojo, rosado y naranja
    umbral_inf_rojo = np.array([0, 50, 50])  # HSV - límite inferior para el rojo
    umbral_sup_rojo = np.array([10, 255, 255])  # HSV - límite superior para el rojo
    umbral_inf_rosa = np.array([150, 50, 50])  # HSV - límite inferior para el rosa
    umbral_sup_rosa = np.array([180, 255, 255])  # HSV - límite superior para el rosa
    umbral_inf_naranja = np.array([10, 50, 50])  # HSV - límite inferior para el naranja
    umbral_sup_naranja = np.array([30, 255, 255])  # HSV - límite superior para el naranja

    # Crear máscaras binarias para rojo, rosado y naranja
    mascara_rojo = cv2.inRange(hsv, umbral_inf_rojo, umbral_sup_rojo)
    mascara_rosa = cv2.inRange(hsv, umbral_inf_rosa, umbral_sup_rosa)
    mascara_naranja = cv2.inRange(hsv, umbral_inf_naranja, umbral_sup_naranja)

    # Calcular el área de cada color en la imagen
    area_rojo = np.sum(mascara_rojo) / 255
    area_rosa = np.sum(mascara_rosa) / 255
    area_naranja = np.sum(mascara_naranja) / 255

    # Obtener el color predominante
    areas = [area_rojo, area_rosa, area_naranja]
    colores = ['Rojo', 'Rosa', 'Naranja']
    color_predominante = colores[np.argmax(areas)]

    return color_predominante

# Ruta de la imagen a procesar
ruta_imagen = 'resultado3.jpg'

# Llamar a la función para reconocer el color predominante
color = reconocer_color(ruta_imagen)

# Imprimir el resultado
print("Color predominante:", color)
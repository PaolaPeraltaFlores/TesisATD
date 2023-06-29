import cv2
import numpy as np

def segment_tongue(image):
    # Convertir la imagen al espacio de color Lab
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # Redimensionar la imagen para facilitar la segmentación
    resized_image = cv2.resize(lab_image, (image.shape[1] // 2, image.shape[0] // 2))

    # Aplicar k-means a la imagen redimensionada
    reshaped_image = resized_image.reshape(resized_image.shape[0] * resized_image.shape[1], 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(reshaped_image, 2, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Asignar etiquetas a la imagen original
    segmented_image = labels.reshape(resized_image.shape[:2])

    # Encontrar la etiqueta dominante (cuerpo de la lengua)
    dominant_label = np.argmax(np.bincount(segmented_image.flatten()))

    # Crear una máscara para el cuerpo de la lengua
    mask = np.uint8(segmented_image == dominant_label)

    # Aplicar la máscara a la imagen original
    segmented_tongue = cv2.bitwise_and(image, image, mask=mask)

    return segmented_tongue


# Cargar la imagen de la lengua
image = cv2.imread('recortar3.jpg')

# Segmentar la lengua
segmented_tongue = segment_tongue(image)

# Mostrar la imagen original y la lengua segmentada
cv2.imshow('Original', image)
cv2.imshow('Segmented Tongue', segmented_tongue)
cv2.waitKey(0)
cv2.destroyAllWindows()

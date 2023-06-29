import cv2
import numpy as np
from sklearn.cluster import KMeans

def segment_tongue(image_path, num_clusters=2):
    # Cargar la imagen
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convertir la imagen al espacio de color Lab
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

    # Obtener los canales L, a y b
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Crear una matriz de características utilizando a_channel y b_channel
    feature_matrix = np.column_stack((a_channel.flatten(), b_channel.flatten()))

    # Aplicar K-means
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(feature_matrix)

    # Obtener las etiquetas de píxeles
    labels = kmeans.labels_

    # Reshape las etiquetas para que coincidan con la forma de la imagen
    labels = np.reshape(labels, (image.shape[0], image.shape[1]))

    # Crear una máscara para separar el cuerpo de la lengua y el revestimiento de la lengua
    tongue_mask = np.zeros_like(labels, dtype=np.uint8)
    tongue_mask[labels == 1] = 255  # Cuerpo de la lengua en blanco
    tongue_mask[labels == 0] = 128  # Revestimiento de la lengua en gris

    # Aplicar la máscara a la imagen original
    segmented_image = cv2.bitwise_and(image, image, mask=tongue_mask)

    # Calcular el porcentaje del cuerpo de la lengua que se muestra en blanco
    tongue_pixels = np.count_nonzero(tongue_mask == 255)
    total_pixels = tongue_mask.shape[0] * tongue_mask.shape[1]
    tongue_percentage = (tongue_pixels / total_pixels) * 100

    # Imprimir el porcentaje del cuerpo de la lengua que se muestra en blanco
    print("Porcentaje del cuerpo de la lengua (blanco): {:.2f}%".format(tongue_percentage))

    # Mostrar la imagen segmentada y la máscara
    cv2.imshow('Segmented Image', segmented_image)
    cv2.imshow('Tongue Mask', tongue_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ejemplo de uso
segment_tongue('recortar3.jpg', num_clusters=2)

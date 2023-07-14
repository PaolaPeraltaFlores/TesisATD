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
    tongue_mask[labels == 1] = 128  # Revestimiento de la lengua en gris
    tongue_mask[labels == 0] = 255  # Cuerpo de la lengua en blanco

    # Calcular el porcentaje del revestimiento de la lengua
    coating_pixels = np.count_nonzero(tongue_mask == 128)
    total_pixels = tongue_mask.shape[0] * tongue_mask.shape[1]
    coating_percentage = (coating_pixels / total_pixels) * 100

    # Imprimir el porcentaje del revestimiento de la lengua
    print("Porcentaje del revestimiento de la lengua: {:.2f}%".format(coating_percentage))

    # Aplicar la máscara a la imagen original
    segmented_image = cv2.bitwise_and(image, image, mask=tongue_mask)

    # Mostrar la imagen segmentada y la máscara
    cv2.imshow('Segmented Image', segmented_image)
    cv2.imshow('Tongue Mask', tongue_mask)
    cv2.imwrite('saburra7.jpg', tongue_mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

# Ejemplo de uso
segment_tongue('recorteimage_c3iqi8s.jpg', num_clusters=2)
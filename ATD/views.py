from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from .models import gallery
from django.views.decorators.csrf import csrf_exempt
from roboflow import Roboflow
import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

def recortarimagen(nameimageprediction):

    imagen = cv2.imread(nameimageprediction)

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
    directorionuevo1 = os.path.join(BASE_DIR, "media", "recorte", "recorte"+ imagen_recortada_final)
    cv2.imwrite(directorionuevo1, imagen_recortada_final)

    # Mostrar la imagen original y la imagen recortada
    #cv2.imshow('Imagen Original', imagen)
    #cv2.imshow('Imagen Recortada', imagen_recortada_final)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

        
@csrf_exempt
def handleMultipleImagesUpload(request):
    if request.method == "POST":
        
        images = request.FILES['images']
        print(images.file)
        name_image = str(images)
        gallery.objects.create(image = images, name_image=name_image)
        uploaded_images = gallery.objects.all()

        nueva_img = gallery.objects.last()
        print("LENGUA"+str(nueva_img.name_image))

        rf = Roboflow(api_key="ezWoyGKUgHzvpZ7l34C3")
        project = rf.workspace().project("tongue-segmentation")
        model = project.version(1).model

        # infer on a local image
        #print(model.predict("lengua1.jpg").json())
        # infer on an image hosted elsewhere
        #print(model.predict("lengua1.jpg").json())

        # save an image annotated with your predictions
        imagendirectorio = os.path.join(BASE_DIR, "media",  name_image )
        print(imagendirectorio)
        directorionuevo = os.path.join(BASE_DIR, "media", "prediccion", "prediccion"+ name_image)
        model.predict(imagendirectorio).save(directorionuevo)
        recortarimagen(directorionuevo)

        return JsonResponse({"images": [{"url": image.image.url, "name": image.name_image} for image in uploaded_images]})
        return render(request, "index.html")
    

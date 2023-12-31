# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import  CreateAPIView, ListAPIView
from .models import Gallery
from django.views.decorators.csrf import csrf_exempt
from roboflow import Roboflow
from .serializer import GallerySerializer
import os
import cv2
import numpy as np
from colorthief import ColorThief
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from ultralytics import YOLO
import threading
from skimage import io
from sklearn.cluster import KMeans
import webcolors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def segment_tongue(image_path, image_create, num_clusters=2):
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
    image_create.porcentaje = str(round(coating_percentage,2))+" %"
    print("Porcentaje del revestimiento de la lengua: {:.2f}%".format(coating_percentage))

    # Aplicar la máscara a la imagen original
    segmented_image = cv2.bitwise_and(image, image, mask=tongue_mask)

    # Mostrar la imagen segmentada y la máscara
    #cv2.imshow('Segmented Image', segmented_image)
    #cv2.imshow('Tongue Mask', tongue_mask)
    directoriosaburra = os.path.join(BASE_DIR, "media", "saburra", "saburra"+image_create.name_image)
    cv2.imwrite(directoriosaburra, tongue_mask)
    image_create.saburra = os.path.join("media", "saburra", "saburra"+image_create.name_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


class ColorAnalyzer:
    def __init__(self, file):
        self.color_thief = ColorThief(file)

    def get_color(self, quality=10):
        return self.color_thief.get_color(quality)

    def get_palette(self, color_count=10, quality=10):
        return self.color_thief.get_palette(color_count, quality)

def analyze_image(image_path, image_create):
    color_analyzer = ColorAnalyzer(image_path)

    dominant_color = color_analyzer.get_color(quality=1)
    palette = color_analyzer.get_palette(color_count=6)

    # Crear una figura y mostrar el color dominante como una imagen
    fig, ax = plt.subplots()
    color_image = np.array([[dominant_color]])
    ax.imshow(color_image)
    ax.axis('off')
    directoriocolordominante = os.path.join(BASE_DIR, "media", "colordominante", "dominante"+image_create.name_image)
    plt.savefig(directoriocolordominante,  bbox_inches='tight', pad_inches=0)
    image_create.color_dominante = os.path.join("media", "colordominante", "dominante"+image_create.name_image)
    #plt.show()

    if palette:
        # Mostrar la paleta de colores como imágenes
        fig, axs = plt.subplots(1, len(palette))
        for i, color in enumerate(palette):
            axs[i].imshow(np.array([[color]]))
            axs[i].axis('off')
        directoriopaleta = os.path.join(BASE_DIR, "media", "paleta", "paleta"+image_create.name_image)
        plt.savefig(directoriopaleta, bbox_inches='tight', pad_inches=0) 
        image_create.paleta_colores = os.path.join("media", "paleta", "paleta"+image_create.name_image)
        #plt.show()
    else:
        print("No se encontraron colores en la paleta.")



def recortarimagen(nameimageprediction, name_image,image_create):
    #print('nombre', name_image)
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
    #print(imagen_recortada_final)
    # Guardar la imagen resultante
    name_image_ref = "recorte"+ str(name_image)

    image_create.name_recortada = os.path.join("media",'recorte', name_image_ref)
    
    directorionuevo1 = os.path.join(BASE_DIR, "media", "recorte", name_image_ref)
    
    
    cv2.imwrite(directorionuevo1, imagen_recortada_final)
    #print('Finalizo')
    directorioimagenrecortada = os.path.join(BASE_DIR, image_create.name_recortada)
    analyze_image(directorioimagenrecortada, image_create)
    segment_tongue(directorioimagenrecortada, image_create, num_clusters=2)
    # Mostrar la imagen original y la imagen recortada
    #cv2.imshow('Imagen Original', imagen)
    #cv2.imshow('Imagen Recortada', imagen_recortada_final)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


class UploadImageCreate(CreateAPIView):
    authentication_classes = []
    serializer_class = GallerySerializer
    def create(self, request, *args, **kwargs):
        print(request.FILES)
        image_create = Gallery.objects.create(
            image = request.FILES['image']
        )
        name_image = str(image_create.image).split('/')[-1]
        image_create.name_image = name_image

        rf = Roboflow(api_key="ezWoyGKUgHzvpZ7l34C3")
        project = rf.workspace().project("tongue-segmentation")
        model = project.version(1).model

        # infer on a local image
        #print(model.predict("lengua1.jpg").json())
        # infer on an image hosted elsewhere
        #print(model.predict("lengua1.jpg").json())

        # save an image annotated with your predictions
        imagendirectorio = os.path.join(BASE_DIR, "media", str(image_create.image))
        name_Image_concat = "prediccion"+ name_image
        directorionuevo = os.path.join(BASE_DIR, "media", "prediccion", name_Image_concat)
        model.predict(imagendirectorio).save(directorionuevo)
        image_create.name_segmentada = os.path.join("media", "prediccion", name_Image_concat)
        recortarimagen(directorionuevo,name_image, image_create)
        
        directorioL = os.path.join(BASE_DIR, "media", "textura")
        foldeName=name_image.split(".")

        model = YOLO('/home/paola/Desktop/TEXTURA/runs/detect/train4/weights/best.pt')
        predictions = model.predict(
        source=imagendirectorio, 
        save=True,
        project=directorioL,
        name=foldeName[0],
        #save_crop=True,
        conf=0.55
        )
        
        print("--")
        #print(predictions)
        #resultado_yolo = os.path.join(BASE_DIR, "media", "prediccion", "textura.jpg")
        #predictions.save(directorionuevo)
        print("--")
        image_create.textura="media/textura/"+foldeName[0]+"/"+name_image
        
        # hilo = threading.Thread(target=recortarimagen, args=[directorionuevo,name_image, image_create])
        # # Iniciar la ejecución del hilo
        # hilo.start()
        # #hilo.join()
        image_create.save()


        serializer = GallerySerializer(image_create)
        return Response({'message':'Successful','data':serializer.data,'code':200})

class ImageList(ListAPIView):
    authentication_classes = []
    queryset = Gallery.objects.all().order_by('-created_at')[:5]
    serializer_class = GallerySerializer
    

class ImagebyID(ListAPIView):
    authentication_classes = []
    serializer_class = GallerySerializer
    def  list(self, request, *args, **kwargs):
        image = Gallery.objects.filter(pk=kwargs.get("pk"))
        serializer = GallerySerializer(image[0])
        if serializer.is_valid:
            return Response ({'message':'Succesful','data':serializer.data,'code':200})
        return Response ({'message':'Error','code':400})
    

class ImagebyIDcolordominante(ListAPIView):
    authentication_classes = []
    serializer_class = GallerySerializer
    
    def verificar_range(self,numero, limite_inferior, limite_superior):
            if numero < limite_inferior:
                diferencia = limite_inferior - numero
                return diferencia
            elif numero > limite_superior:
                diferencia = numero - limite_superior 
                return diferencia
            else:
                return "dentro del rango"
            
    def calcular_color (self, R, G, B, rmin, rmax, gmin, gmax, bmin, bmax, nombrecolor, descripcion):
            contador_colores = 0
            pertenecer = True
            perteneceg = True
            perteneceb = True

            if int(R) >= int(rmin) and int(R) <= int(rmax):
                contador_colores = contador_colores+ 1 
            else: 
                pertenecer = False

            if G >= gmin and G <= gmax:
                contador_colores += 1  
            else: 
                perteneceg = False

            if B >= bmin and B <= bmax:
                contador_colores += 1
            else: 
                perteneceb = False
            print(contador_colores)
            if contador_colores >= 2:
                print('El color pertenece a al menos dos colores de la gama'+nombrecolor)
                resultado = 0
                if pertenecer == False:
                    resultado = self.verificar_range(R, rmin, rmax)

                if perteneceg == False:
                    resultado = self.verificar_range(G, gmin, gmax)

                if perteneceb == False:
                    resultado = self.verificar_range(B, bmin, bmax)

                #arrayresultado.append({"valor":resultado,"tipo":"palido"})
                return {"valor":resultado,"tipo":nombrecolor, "descripcion":descripcion}
            return False
            

    def  list(self, request, *args, **kwargs):
        image = Gallery.objects.filter(pk=kwargs.get("pk"))
        serializer = GallerySerializer(image[0])
        if serializer.is_valid:
            print(serializer['color_dominante'].value)
            directoriocolorrgb = os.path.join(BASE_DIR, serializer['color_dominante'].value)
            # Cargar la imagen
            imagen = io.imread(directoriocolorrgb)

            # Obtener las dimensiones de la imagen
            alto, ancho, _ = imagen.shape

            # Redimensionar la imagen para facilitar el procesamiento
            imagen_redimensionada = imagen.reshape(alto * ancho, 3)

            # Aplicar el algoritmo de K-Means para encontrar los colores dominantes
            kmeans = KMeans(n_clusters=1, n_init=10)  # Establecer n_init en 10
            kmeans.fit(imagen_redimensionada)

            # Obtener los colores dominantes
            colores_dominantes = kmeans.cluster_centers_

            # Convertir los valores de los colores a enteros
            colores_dominantes = colores_dominantes.round().astype(int)

            print(colores_dominantes)
            # Definir vector auxiliar
            color = colores_dominantes[0]
            print (color)
            R = color[0]
            G = color[1]
            B = color[2]

            #Color Palido
            rvpmin = 235
            rvpmax = 260
            gvpmin = 230
            gvpmax = 255
            bvpmin = 230
            bvpmax = 255

            #Color Rosa
            rvrmin = 225
            rvrmax = 265
            gvrmin = 90
            gvrmax = 217
            bvrmin = 125
            bvrmax = 226

            #Color Rojo rv1
            rv1min = 214
            rv1max = 260
            gv1min = 0
            gv1max = 60
            bv1min = 45
            bv1max = 105

            #Color ROjo INtenso rv2
            rv2min = 90
            rv2max = 250
            gv2min = 0
            gv2max = 60
            bv2min = 0
            bv2max = 70

            #Color Violeta
            rvvmin = 144
            rvvmax = 210
            gvvmin = 35
            gvvmax = 150
            bvvmin = 90
            bvvmax = 215

            #COlor Azul
            rvamin = 165
            rvamax = 210
            gvamin = 190
            gvamax = 215
            bvamin = 195
            bvamax = 240

            arrayresultado=[]

            #palido
            descpalido = "El color de su lengua pertenece a la gama del color Pálido, el cual puede indicar una mala circulación de sangre."
            resultadopalido = self.calcular_color(R, G, B, rvpmin, rvpmax, gvpmin, gvpmax, bvpmin, bvpmax, 'palido', descpalido)
            print(resultadopalido)
            if resultadopalido !=  False:
                arrayresultado.append(resultadopalido)

            #rosado 
            descrosado = "El color de su lengua pertenece a la gama del color Rosado, siendo este el color normal en una persona saludable."
            resultadorosado = self.calcular_color(R, G, B, rvrmin, rvrmax, gvrmin, gvrmax, bvrmin, bvrmax, 'rosado', descrosado)
            print(resultadorosado)
            if resultadorosado !=  False:
                arrayresultado.append(resultadorosado)

            #rojo
            descrojo = "El color de su lengua pertenece a la gama del color Rojo. En algunas ocasiones se presenta como el color normal de la lengua, sin embargo, puede tener implicaciones patológicas."
            resultadorojo = self.calcular_color(R, G, B, rv1min, rv1max, gv1min, gv1max, bv1min, bv1max, 'rojo', descrojo)
            print(resultadorojo)
            if resultadorojo !=  False:
                arrayresultado.append(resultadorojo)

            #rojo intenso
            descintenso = "El color de su lengua pertenece a la gama del color Rojo Intenso. Este color puede indicar un aumento de temperatura en el cuerpo."
            resultadorojointenso = self.calcular_color(R, G, B, rv2min, rv2max, gv2min, gv2max, bv2min, bv2max, 'rojo intenso', descintenso)
            print(resultadorojointenso)
            if resultadorojointenso !=  False:
                arrayresultado.append(resultadorojointenso)

            #violeta
            descvioleta = "El color de su lengua pertenece a la gama del color Violeta. Este color puede observarse durante el desarrollo de una enfermedad."
            resultadovioleta = self.calcular_color(R, G, B, rvvmin, rvvmax, gvvmin, gvvmax, bvvmin, bvvmax, 'violeta', descvioleta)
            print(resultadovioleta)
            if resultadovioleta !=  False:
                arrayresultado.append(resultadovioleta)

            #azul
            descazul = "El color de su lengua pertenece a la gama del color Azul. Este color puede ser un indicativo de frío en el cuerpo y puede verse afectado su hígado y riñón."
            resultadoazul = self.calcular_color(R, G, B, rvamin, rvamax, gvamin, gvamax, bvamin, bvamax, 'azul', descazul)
            print(resultadoazul)
            if resultadoazul !=  False:
                arrayresultado.append(resultadoazul)

            print(arrayresultado)

            colorResultante = ''
            colormenor = min(arrayresultado, key=lambda p: p['valor'])
            colorResultante = colormenor['tipo']
            descripcionresultante = colormenor['descripcion']
            print(colorResultante)
            return Response ({'message':'Succesful','data':colorResultante, 'descripcion':descripcionresultante, 'code':200})
        return Response ({'message':'Error','code':400})
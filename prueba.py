from skimage import io
from sklearn.cluster import KMeans
import webcolors

def verificar_range(numero, limite_inferior, limite_superior):
    if numero < limite_inferior:
        diferencia = limite_inferior - numero
        return diferencia
    elif numero > limite_superior:
        diferencia = numero - limite_superior 
        return diferencia
    else:
        return "dentro del rango"
    
def calcular_color (R, G, B, rmin, rmax, gmin, gmax, bmin, bmax, nombrecolor):
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
            resultado = verificar_range(R, rmin, rmax)

        if perteneceg == False:
            resultado = verificar_range(G, gmin, gmax)

        if perteneceb == False:
            resultado = verificar_range(B, bmin, bmax)

        #arrayresultado.append({"valor":resultado,"tipo":"palido"})
        return {"valor":resultado,"tipo":nombrecolor}
    return False
    

# Cargar la imagen
imagen = io.imread('colordo.jpg')

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
resultadopalido = calcular_color(R, G, B, rvpmin, rvpmax, gvpmin, gvpmax, bvpmin, bvpmax, 'palido')
print(resultadopalido)
if resultadopalido !=  False:
    arrayresultado.append(resultadopalido)

#rosado 
resultadorosado = calcular_color(R, G, B, rvrmin, rvrmax, gvrmin, gvrmax, bvrmin, bvrmax, 'rosado')
print(resultadorosado)
if resultadorosado !=  False:
    arrayresultado.append(resultadorosado)

#rojo
resultadorojo = calcular_color(R, G, B, rv1min, rv1max, gv1min, gv1max, bv1min, bv1max, 'rojo')
print(resultadorojo)
if resultadorojo !=  False:
    arrayresultado.append(resultadorojo)

#rojo intenso
resultadorojointenso = calcular_color(R, G, B, rv2min, rv2max, gv2min, gv2max, bv2min, bv2max, 'rojo intenso')
print('intenso',resultadorojointenso)
if resultadorojointenso !=  False:
    arrayresultado.append(resultadorojointenso)

#violeta
resultadovioleta = calcular_color(R, G, B, rvvmin, rvvmax, gvvmin, gvvmax, bvvmin, bvvmax, 'violeta')
print(resultadovioleta)
if resultadovioleta !=  False:
    arrayresultado.append(resultadovioleta)

#azul
resultadoazul = calcular_color(R, G, B, rvamin, rvamax, gvamin, gvamax, bvamin, bvamax, 'azul')
print(resultadoazul)
if resultadoazul !=  False:
    arrayresultado.append(resultadoazul)

print(arrayresultado)

colorResultante = ''
colormenor = min(arrayresultado, key=lambda p: p['valor'])
colorResultante = colormenor['tipo']
print(colorResultante)
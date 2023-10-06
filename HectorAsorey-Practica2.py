from functools import reduce
from io import BytesIO
from PIL import Image
import requests

####################################################

def es_palindromo_aux(mi_string):
    stringUpper = mi_string.upper()
    stringAnalyze = stringUpper.replace(' ', '')
    if stringAnalyze == stringAnalyze[::-1]:
        return f"'{mi_string}' es palindromo"
    else:
        return f"'{mi_string}' no es palindromo"

def es_palindromo(lista_strings):
    resultado = map(es_palindromo_aux, lista_strings)
    print(list(resultado))
    return(list(resultado))

####################################################

es_palindromo(['Hola', 'Ana', 'Aba', 'Adios', 'Uno', 'Alla', 'Palabra', 'String', 'Integer', 'Palindromo'])
es_palindromo(['Mando', 'Tele', 'Consola', 'Movil', 'Ordenador', 'Portatil', 'Altavoz', 'Cascos', 'Reloj', 'Cargador'])
es_palindromo(['Ama', 'Eme', 'Erre', 'Nadan', 'Oro', 'Oso', 'Radar', 'Rallar', 'Rotor', 'Sus'])
es_palindromo(['Salas', 'Sedes', 'Seres', 'Solos', 'Somos', 'Libro', 'Linterna', 'Litera', 'Llama', 'Luz'])
es_palindromo(['Oscuridad', 'Aerea', 'Espartano', 'Ene', 'Viajero', 'Ojo', 'Galaxia', 'Rotomotor', 'Catana', 'Rallar'])

####################################################

def impares_de(lista_n):
    resultado = filter(lambda x: x%2 == 1, lista_n)
    print(list(resultado))
    return(list(resultado))

####################################################

impares_de([1,2,3,4,5,6,7,8,9])
impares_de([11,12,13,14,15,16,17,18,19])
impares_de([111,112,113,114,115,116,117,118,119])
impares_de([17,27,37,47,57,67,77,87,97])
impares_de([1,2,4,6,8,10,12,14,16])

####################################################

def cuadrados_sumados(n):
    lista = range(1, n+1)
    #resultado = map(lambda x: x**2, lista)
    resultado = reduce(lambda x,y: x+y, map(lambda x: x**2, lista))
    print("La suma de los cuadrados de 1 a " + str(n) + " es: " + str(resultado))
    return resultado

####################################################

cuadrados_sumados(4)
cuadrados_sumados(5)
cuadrados_sumados(6)
cuadrados_sumados(7)
cuadrados_sumados(8)

####################################################

def factorial(n):
    if n > 0:
        resultado = reduce(lambda x,y: x*y, range(1, n+1))
        print("El factorial de " + str(n) + " es: " + str(resultado))
    else:
        resultado = 1
        print("El factorial de " + str(n) + " es: " + str(resultado))
    return resultado

####################################################

factorial(4)
factorial(1)
factorial(13)
factorial(7)
factorial(0)

####################################################

def imagen_fichero(ruta):
    return Image.open(ruta)

def imagen_web(url):
    return Image.open(BytesIO(requests.get(url).content))
    #return Image.open(urllib.request.urlretrieve(url))
    
def img_to_bw(funcion):
    img = funcion
    img = img.resize((720,405), Image.ANTIALIAS)
    img = img.convert("L")
    img.show()
    return img

####################################################

#img_to_bw(imagen_fichero("/home/hector/Imágenes/Wallpapers/aaa.jpg"))
#img_to_bw(imagen_fichero("/home/hector/Imágenes/Wallpapers/Halo.jpg"))
#img_to_bw(imagen_web("https://wpassets.halowaypoint.com/wp-content/2021/10/Autumnarchives_thumbnail-2.jpg"))
#img_to_bw(imagen_web("https://wpassets.halowaypoint.com/wp-content/2022/12/HI-DecUpdate-Header.jpg"))
#img_to_bw(imagen_web("https://wpassets.halowaypoint.com/wp-content/2021/11/Lassen_KeyArt_Flat_NoLogo-scaled.jpg"))


def ejercicio(lista):
    return reduce(lambda x,y: x if x >= y else y, lista)

print(ejercicio([1,2,3,4,5,6,7,8]))

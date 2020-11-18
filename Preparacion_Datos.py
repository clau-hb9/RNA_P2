import csv
import random
from random import sample
import numpy as np

""" Directorios """
carpeta_DatosProcesados = 'DatosProcesados/'
DatosEntrada = 'datosNubes'
extension = '.dat'
extension_salida = ".txt"



""" Función para normalizar cada valor """
def normalizacion(dato, minimo, maximo):
    return float((dato - minimo)/(maximo - minimo))

""" Calculamos el valor mínimo de una columna """
def valor_minimo(datosEntrada,columna):
    #Definimos el valor minimo inicial como el primer valor encontrado en la columna
    minimo= float(datosEntrada[0][columna])
    for fila in datosEntrada:
        #Comparamos el valor de la fila que estamos recorriendo en la columna deseada y lo comparamos con el minimo actual
        if float(fila[columna]) < minimo:
            #Si ese valor es menor --> cambiamos este al valor minimo
            minimo = float(fila[columna])
    #Cuando recorramos y comparemos todos los valores de esa columna --> devolvemos el minimo encontrado
    return minimo

""" Calculamos el valor máximo de una columna """
def valor_maximo(datosEntrada,columna):
    #Definimos el valor máximo inicial como el primer valor encontrado en la columna
    maximo= float(datosEntrada[0][columna])
    for fila in datosEntrada:
        #Comparamos el valor de la fila que estamos recorriendo en la columna deseada y lo comparamos con el maximo actual
        if float(fila[columna]) > maximo:
            #Si ese valor es mayor --> cambiamos este al valor maximo
            maximo = float(fila[columna])
    #Cuando recorramos y comparemos todos los valores de esa columna --> devolvemos el maximo encontrado
    return maximo

""" Función para guardar los valores máximos y mínimos de cada columna en un fichero (se utilizará posteriormente para desnormalizar) """
def save_max_min(categorias, datos_sinCategoria):
    lista_maximos= []
    lista_minimos= []
    #Para cada columna calculamos su minimo y maximo y lo guardamos y nuestra lista
    for columna in range(len(categorias)-1):
        lista_maximos.append(valor_maximo(datos_sinCategoria,columna))
        lista_minimos.append(valor_minimo(datos_sinCategoria,columna))
    #Generamos un fichero donde escribimos estos datos
    with open(carpeta_DatosProcesados + DatosEntrada + '_MaximoMinimo' + extension_salida, mode='w', newline='') as fichero_salida:
        writer = csv.writer(fichero_salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        #Escribimos los nombres de las columnas
        writer.writerow(categorias)
        #Debajo de cada columa escribimos los maximos
        writer.writerow(lista_maximos)
        #Debajo de cada columa escribimos los minimos
        writer.writerow(lista_minimos)
    
    return lista_maximos, lista_minimos

""" Funcion para generar los ficheros de salida de datos """
def generar_fichero(nombre, modelo, data, categorias):
    # Abrimos el fichero donde vamos a escribir
    with open(carpeta_DatosProcesados + modelo + DatosEntrada + nombre + extension_salida, mode='w', newline='') as fichero_salida:
        writer = csv.writer(fichero_salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        #Escribimos las categorias
        writer.writerow(categorias)
        
        #Escribimos en sus ficheros respectivos los datos
        for x in range(len(data)):
            writer.writerow(data[x])
    return fichero_salida


""" Función para aleatorizar las filas """
def aleatorizacion(datos_sinCategoria):
    datos_aleatorios = sample(datos_sinCategoria, len(datos_sinCategoria))
    return datos_aleatorios

""" Función que lee los datos del fichero de entrada """
def lectura_DatosEntrada():
    datosEntrada= []
    #Primero abrimos el fichero
    with open(DatosEntrada + extension, mode='r') as FicheroEntrada:
         #Leemos cada campo, que esta separado por comas
        reader = csv.reader(FicheroEntrada, delimiter=',')
        #Guardamos en nuestra variable datosEntrada cada fila leída
        for fila in reader:
            datosEntrada.append(fila)
    return datosEntrada


""" Función para leer un fichero csv y devolverlo en una lista """
def leer():
    # Abrimos el fichero
    with open(DatosEntrada + extension, mode='r') as fichero_csv:
        # Lo leemos
        csv_reader = csv.reader(fichero_csv, delimiter=',')
        # Quitamos las cabeceras
        next(csv_reader)
        array = []
        for i, row in enumerate(csv_reader):
            array.append([])
            for j, value in enumerate(row):
                if (j!=12):
                    array[i].append(float(value))
                else:
                    array[i].append(value)
        return array

""" Main """
def main():
    #Primero leemos los datos del fichero de entrada
    datos = lectura_DatosEntrada()
    cabeceras = datos[0]
    datos_sinCategoria = leer()
    #Guardamos los maximos y minimos de cada columna
    maximos, minimos = save_max_min(cabeceras, datos_sinCategoria)

    #Calculamos los datos normalizados
    datos_normalizados = []
    for num_fila, contenidoCompleto_fila in enumerate(datos_sinCategoria):
        datos_normalizados.append([])
        for columna, valor in enumerate(contenidoCompleto_fila[:-1]):
            datoNormalizado = normalizacion(valor, minimos[columna], maximos[columna])
            datos_normalizados[num_fila].append(datoNormalizado)
        datos_normalizados[num_fila].append(contenidoCompleto_fila[12])

    #Dividir en clases
    datos_nubes = []
    datos_cieloDespejado= []
    datos_multinube = []
    
    
    for x in range(len(datos_normalizados)):
        var = datos_normalizados[x][12]
        if(var == "nube"):
            datos_nubes.append(datos_normalizados[x])
        elif(var == "cieloDespejado"):
            datos_cieloDespejado.append(datos_normalizados[x])
        else:
            datos_multinube.append(datos_normalizados[x])


    """ CANTIDAD DE DATOS EN CADA FOLD
        12 --> datos_cieloDespejado
        39 --> datos_multinube
        129+128+128+128 --> datos_nube  """

    P1, P2, P3, P4 = [], [], [], []
    for x in range(len(datos_cieloDespejado)):
        if (x < 12):
            P1.append(datos_cieloDespejado[x])
        elif (x >= 12 and x < 24):
            P2.append(datos_cieloDespejado[x])
        elif (x >= 24 and x < 36):
            P3.append(datos_cieloDespejado[x])
        else:
            P4.append(datos_cieloDespejado[x])
    
    for x in range(len(datos_multinube)):
        if (x < 39):
            P1.append(datos_multinube[x])
        elif (x >= 39 and x < 78):
            P2.append(datos_multinube[x])
        elif (x >= 78 and x < 117):
            P3.append(datos_multinube[x])
        else:
            P4.append(datos_nubes[x])

    for x in range(len(datos_nubes)):
        if (x < 129):
            P1.append(datos_nubes[x])
        elif (x >= 129 and x < 257):
            P2.append(datos_nubes[x])
        elif (x >= 257 and x < 385):
            P3.append(datos_nubes[x])
        else:
            P4.append(datos_nubes[x])
    
    # Aleatorizamos todos los conjuntos de datos
    P1_aleatorizado = aleatorizacion(P1)
    P2_aleatorizado = aleatorizacion(P2)
    P3_aleatorizado = aleatorizacion(P3)
    P4_aleatorizado = aleatorizacion(P4)


    # MODELO 1: P1 TEST + (P2+P3+P4) ENTRENAMIENTO
    Conjunto_entrenamiento = P2_aleatorizado + P3_aleatorizado + P4_aleatorizado
    Conjunto_entrenamiento_aleatorizar = aleatorizacion(Conjunto_entrenamiento)
    generar_fichero('_entrenamiento', 'Modelo_1/', Conjunto_entrenamiento_aleatorizar, cabeceras)
    generar_fichero('_test','Modelo_1/', P1_aleatorizado, cabeceras)

    # MODELO 2: P2 TEST +(P1+P3+P4) ENTRENAMIENTO
    Conjunto_entrenamiento = P1_aleatorizado + P3_aleatorizado + P4_aleatorizado
    Conjunto_entrenamiento_aleatorizar = aleatorizacion(Conjunto_entrenamiento)
    generar_fichero('_entrenamiento','Modelo_2/', Conjunto_entrenamiento_aleatorizar, cabeceras)
    generar_fichero('_test', 'Modelo_2/',P2_aleatorizado, cabeceras)

    # MODELO 3: P3 TEST +(P1+P2+P4) ENTRENAMIENTO
    Conjunto_entrenamiento = P1_aleatorizado + P2_aleatorizado + P4_aleatorizado
    Conjunto_entrenamiento_aleatorizar = aleatorizacion(Conjunto_entrenamiento)
    generar_fichero('_entrenamiento','Modelo_3/', Conjunto_entrenamiento_aleatorizar, cabeceras)
    generar_fichero('_test', 'Modelo_3/',P3_aleatorizado, cabeceras)

    # MODELO 4: P4 TEST +(P1+P3+P2) ENTRENAMIENTO
    Conjunto_entrenamiento = P1_aleatorizado + P2_aleatorizado + P3_aleatorizado
    Conjunto_entrenamiento_aleatorizar = aleatorizacion(Conjunto_entrenamiento)
    generar_fichero('_entrenamiento','Modelo_4/', Conjunto_entrenamiento_aleatorizar, cabeceras)
    generar_fichero('_test', 'Modelo_4/',P4_aleatorizado, cabeceras)

    
   
if __name__ == '__main__':
    main()
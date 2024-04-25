import heapq
import os

# Definición de la clase NodoHuffman
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter  # El carácter almacenado en este nodo del árbol
        self.frecuencia = frecuencia  # La frecuencia del carácter en el texto
        self.izquierda = None  # Referencia al nodo hijo izquierdo
        self.derecha = None  # Referencia al nodo hijo derecho

    # Método de comparación para la clase NodoHuffman, necesario para la cola de prioridad
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función para contar la frecuencia de cada carácter en un texto
def contar_frecuencias(texto):
    frecuencias = {}
    for caracter in texto:
        if caracter in frecuencias:
            frecuencias[caracter] += 1
        else:
            frecuencias[caracter] = 1
    return frecuencias

# Función para construir el árbol de Huffman a partir de las frecuencias
def construir_arbol(frecuencias):
    cola = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(cola)
    while len(cola) > 1:
        izquierda = heapq.heappop(cola)
        derecha = heapq.heappop(cola)
        suma_frecuencias = izquierda.frecuencia + derecha.frecuencia
        nodo_padre = NodoHuffman(None, suma_frecuencias)
        nodo_padre.izquierda = izquierda
        nodo_padre.derecha = derecha
        heapq.heappush(cola, nodo_padre)
    return cola[0]

# Función para construir la tabla de códigos Huffman
def construir_tabla_codigos(arbol_huffman, prefijo="", tabla_codigos={}):
    if arbol_huffman is not None:
        if arbol_huffman.caracter is not None:
            tabla_codigos[arbol_huffman.caracter] = prefijo
        construir_tabla_codigos(arbol_huffman.izquierda, prefijo + "0", tabla_codigos)
        construir_tabla_codigos(arbol_huffman.derecha, prefijo + "1", tabla_codigos)
    return tabla_codigos

# Función para comprimir un texto utilizando el algoritmo de Huffman
def comprimir(texto):
    # Contar las frecuencias de cada carácter en el texto
    frecuencias = contar_frecuencias(texto)
    # Construir el árbol de Huffman a partir de las frecuencias
    arbol_huffman = construir_arbol(frecuencias)
    # Construir la tabla de códigos Huffman
    tabla_codigos = construir_tabla_codigos(arbol_huffman)
    # Codificar el texto utilizando la tabla de códigos Huffman
    texto_codificado = ''.join(tabla_codigos[caracter] for caracter in texto)
    # Agregar padding si es necesario para que la longitud del texto codificado sea un múltiplo de 8
    padding = 8 - len(texto_codificado) % 8
    texto_codificado += padding * '0'
    # Convertir el texto codificado a bytes
    bytes_codificados = bytearray()
    for i in range(0, len(texto_codificado), 8):
        byte = texto_codificado[i:i+8]
        bytes_codificados.append(int(byte, 2))
    return bytes_codificados, arbol_huffman, texto_codificado

# Función para descomprimir un texto comprimido
def descomprimir(bytes_codificados, arbol_huffman):
    # Convertir los bytes codificados de vuelta al texto codificado
    texto_codificado = ''.join(f'{byte:08b}' for byte in bytes_codificados)
    # Remover el padding agregado durante la compresión
    padding = texto_codificado[-8:]
    padding = padding.rstrip('0')
    texto_codificado = texto_codificado[:-len(padding)]
    # Decodificar el texto utilizando el árbol de Huffman
    texto_decodificado = ''
    nodo_actual = arbol_huffman
    for bit in texto_codificado:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        if nodo_actual.caracter is not None:
            texto_decodificado += nodo_actual.caracter
            nodo_actual = arbol_huffman
    return texto_decodificado

# Función para comprimir un archivo de texto
def comprimir_archivo(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as f:
        texto = f.read()
    # Comprimir el texto y obtener el árbol de Huffman y el texto codificado
    bytes_codificados, arbol_huffman, texto_codificado = comprimir(texto)
    # Imprimir el texto codificado
    print("Texto comprimido:")
    print(texto_codificado)
    # Escribir los bytes codificados en el archivo de salida
    with open(archivo_salida, 'wb') as f:
        f.write(bytes_codificados)
    return arbol_huffman

# Función para descomprimir un archivo comprimido
def descomprimir_archivo(archivo_entrada, archivo_salida, arbol_huffman):
    # Leer los bytes codificados del archivo de entrada
    with open(archivo_entrada, 'rb') as f:
        bytes_codificados = bytearray(f.read())
    # Descomprimir los bytes y obtener el texto decodificado
    texto_decodificado = descomprimir(bytes_codificados, arbol_huffman)
    # Imprimir el texto decodificado
    print("Texto descomprimido:")
    print(texto_decodificado)
    # Escribir el texto decodificado en el archivo de salida
    with open(archivo_salida, 'w') as f:
        f.write(texto_decodificado)

# Ejemplo de uso
archivo_entrada = 'input.txt'
archivo_comprimido = 'texto.bin'
archivo_descomprimido = 'texto_descomprimido.txt'

# Comprimir el archivo de entrada y guardar el árbol de Huffman para su posterior uso en la descompresión
arbol_huffman = comprimir_archivo(archivo_entrada, archivo_comprimido)

# Descomprimir el archivo comprimido utilizando el árbol de Huffman previamente obtenido
descomprimir_archivo(archivo_comprimido, archivo_descomprimido, arbol_huffman)

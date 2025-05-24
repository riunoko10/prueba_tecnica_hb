def ordenar_bloques(myArray):
    """
    Ordena los números dentro de los bloques de un arreglo y los imprime.
    Valida si el arreglo está vacío antes de procesar.

    Args:
        myArray: Una tupla o lista que contiene números del 1 al 9 y ceros
                 como separadores de bloques.
    """
    # --- VALIDACIÓN ---
    # Verificamos si el arreglo está vacío o no tiene elementos.
    if not myArray:
        print("El arreglo está vacío y no se procesará.")
        return  # Salimos de la función si está vacío

    # --- PROCESAMIENTO (Si no está vacío) ---
    bloques_procesados = []
    bloque_actual = []

    # Iteramos sobre cada número en el arreglo de entrada
    for numero in myArray:
        if numero == 0:
            # Si encontramos un cero, procesamos el bloque actual
            if not bloque_actual:
                # Si el bloque está vacío, añadimos 'X'
                bloques_procesados.append('X')
            else:
                # Si no está vacío, lo ordenamos y lo convertimos a string
                bloque_actual.sort()
                bloques_procesados.append(''.join(map(str, bloque_actual)))
            # Reiniciamos el bloque actual para empezar uno nuevo
            bloque_actual = []
        else:
            # Si no es cero, lo añadimos al bloque actual
            bloque_actual.append(numero)

    # No olvides procesar el último bloque después de terminar el bucle
    if not bloque_actual:
        bloques_procesados.append('X')
    else:
        bloque_actual.sort()
        bloques_procesados.append(''.join(map(str, bloque_actual)))

    # Imprimimos los bloques procesados, separados por un espacio
    print(' '.join(bloques_procesados))

if __name__ == '__main__':
    entrada_1 = [1,3,2,0,7,8,1,3,0,6,7,1]
    entrada_2 = [2,1,0,0,3,4]
    entrada_3 = [2,1,0,0,3,4,0,0,0,123,1,2,3]
    entrada_4 =[]

    entradas = [entrada_1, entrada_2, entrada_3, entrada_4]

    for entrada in entradas:
        salida = ordenar_bloques(entrada)
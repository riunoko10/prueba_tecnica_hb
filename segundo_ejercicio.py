def ordenar_bloques(myArray):
    """
    Ordena los números dentro de los bloques de un arreglo y los imprime.
    Valida si el arreglo está vacío antes de procesar.

    Args:
        myArray: Una tupla o lista que contiene números del 1 al 9 y ceros
                 como separadores de bloques.
    """
    # --- VALIDACIÓN ---
    if not myArray:
        print("El arreglo está vacío y no se procesará.")
        return

    # --- PROCESAMIENTO ---
    bloques_procesados = []
    bloque_actual = []

    # Iteramos sobre cada número en el arreglo de entrada
    for numero in myArray:
        if numero == 0:
            # Si encontramos un cero, procesamos el bloque actual
            bloques_procesados.append(_procesar_bloque(bloque_actual))
            bloque_actual = []  # Reiniciamos el bloque actual
        else:
            # Si no es cero, lo añadimos al bloque actual
            bloque_actual.append(numero)

    # Procesamos el último bloque después de terminar el bucle
    bloques_procesados.append(_procesar_bloque(bloque_actual))

    # Imprimimos los bloques procesados, separados por un espacio
    print(' '.join(bloques_procesados))


def _procesar_bloque(bloque):
    """
    Procesa un bloque individual ordenándolo o devolviendo 'X' si está vacío.
    
    Args:
        bloque: Lista de números para procesar
        
    Returns:
        str: Bloque ordenado como string o 'X' si está vacío
    """
    if not bloque:
        return 'X'
    else:
        bloque.sort()
        return ''.join(map(str, bloque))


def main():
    """Función principal que ejecuta los casos de prueba"""
    casos_prueba = [
        [1, 3, 2, 0, 7, 8, 1, 3, 0, 6, 7, 1],
        [2, 1, 0, 0, 3, 4],
        [2, 1, 0, 0, 3, 4, 0, 0, 0, 1, 2, 3],
        []
    ]

    for i, caso in enumerate(casos_prueba, 1):
        print(f"Caso {i}: {caso}")
        ordenar_bloques(caso)
        print()


if __name__ == '__main__':
    main()
import time

def calcular_tiempo_transcurrido(inicio, fin):
    """
    Calcula el tiempo transcurrido en milisegundos.
    """
    return int((fin - inicio) * 1000)

def guardar_resultados(tiempo_ms, seleccionadas_a, seleccionadas_e, seleccionadas_r, errores, bostezos, selecionTotal, omisiones, porcentaje_fatiga):
    """
    Guarda los resultados en un archivo de texto llamado 'resultados2.txt'.
    """
    with open("resultados2.txt", "w") as archivo:
        archivo.write(f"Tiempo empleado: {tiempo_ms} ms\n")
        archivo.write(f"Letras 'A' seleccionadas: {seleccionadas_a}\n")
        archivo.write(f"Letras 'E' seleccionadas: {seleccionadas_e}\n")
        archivo.write(f"Letras 'R' seleccionadas: {seleccionadas_r}\n")
        archivo.write(f"Letras incorrectas seleccionadas: {errores}\n")
        archivo.write(f"Letras correctas seleccionadas: {selecionTotal}\n")
        archivo.write(f"Letras omitidas: {omisiones}\n")
        archivo.write(f"Bostezos detectados: {bostezos}\n")  # Agregar bostezos detectados
        archivo.write(f"Porcentaje de fatiga: {porcentaje_fatiga:.2f}%\n")

    print("Resultados guardados en 'resultados2.txt'.")

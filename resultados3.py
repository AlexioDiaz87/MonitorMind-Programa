import time

def calcular_tiempo_transcurrido(inicio, fin):
    """
    Calcula el tiempo transcurrido en milisegundos.
    """
    return int((fin - inicio) * 1000)

def guardar_resultados(tiempo_ms, triangulos_seleccionados, errores_seleccionados, bostezos):
    """
    Guarda los resultados en un archivo de texto llamado 'resultados3.txt'.
    """
    with open("resultados3.txt", "w") as archivo:
        archivo.write(f"Tiempo empleado: {tiempo_ms} ms\n")
        archivo.write(f"Triángulos seleccionados: {triangulos_seleccionados}\n")
        archivo.write(f"Figuras erróneas seleccionadas: {errores_seleccionados}\n")
        archivo.write(f"Bostezos detectados: {bostezos}\n")  # Guardar bostezos detectados

    print("Resultados guardados en 'resultados3.txt'.")

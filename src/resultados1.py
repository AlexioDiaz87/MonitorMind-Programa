# resultados.py

def calcular_igap(aciertos, errores, omisiones):
    """
    Calcula el IGAP usando la fórmula: IGAP = A - (E + O)
    """
    return aciertos - (errores + omisiones)

def calcular_capacidad_perceptiva(aciertos, errores, omisiones):
    """
    Calcula el porcentaje de capacidad perceptiva basado en aciertos, errores y omisiones.
    """
    total_respuestas = aciertos + errores + omisiones
    if total_respuestas == 0:
        return 0  # Evitar división por cero
    return round((aciertos / total_respuestas) * 100, 2)


def guardar_resultados(aciertos, errores, omisiones, igap):
    """
    Guarda los resultados en un archivo de texto llamado 'resultados.txt'.
    """

    capacidad_perceptiva = calcular_capacidad_perceptiva(aciertos, errores, omisiones)

    with open("resultados.txt", "w") as archivo:
        archivo.write(f"Aciertos: {aciertos}\n")
        archivo.write(f"Errores: {errores}\n")
        archivo.write(f"Omisiones: {omisiones}\n")
        archivo.write(f"IGAP: {igap}\n")
        archivo.write(f"Capacidad Perceptiva: {capacidad_perceptiva}%\n")  # Guardar porcentaje
    print("Resultados guardados en 'resultados.txt'.")
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Agrega el directorio actual al path
import resultados

# Variable global para almacenar el conteo de bostezos
resultados = 0

def contar_bostezos():
    """Función para contar bostezos durante el test."""
    global resultados
    resultados += 1

def show_results(start_time, end_time, times, correct_clicks, errors):
    """Función para calcular y mostrar los resultados del test."""
    total_time = end_time - start_time
    transitions = [times[i] - times[i - 1] for i in range(1, len(times))]
    avg_transition_time = sum(transitions) / len(transitions) if transitions else 0
    efficiency = correct_clicks / (correct_clicks + len(errors)) if (correct_clicks + len(errors)) > 0 else 0

    # Resultados del test
    results = f"Resultados:\n"
    results += f"- Tiempo Total: {total_time:.2f} segundos\n"
    results += f"- Tiempo Promedio por Cuadro: {avg_transition_time:.2f} segundos\n"
    results += f"- Eficiencia: {efficiency * 100:.2f}%\n"
    results += f"- Errores Totales: {len(errors)}\n"
    results += f"- Bostezos Totales: {resultados}\n"

    if errors:
        results += f"Errores por Cuadro: {errors}\n"

    # Mostrar los resultados
    messagebox.showinfo("Resultados", results)

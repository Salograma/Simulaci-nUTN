"""
Función genérica de diagnóstico visual para generadores pseudoaleatorios.
Aplicable a cualquier secuencia de valores en [0, 1).

Gráficos generados:
    1. Histograma de frecuencias
    2. Diagrama de dispersión u(n) vs u(n+1)
    3. Serie temporal (primeros 200 valores)
    4. Distribución empírica vs teórica U[0,1) (KS)

Parámetros
datos  : secuencia de valores en [0, 1)
nombre : nombre del generador (usado en títulos y nombre del archivo)
"""

import numpy as np
import matplotlib.pyplot as plt


def graficar(datos: list[float], nombre: str = "Generador") -> None:

    n = len(datos)
    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle(f"Diagnóstico del generador: {nombre}", fontsize=14)

    # 1. Histograma de frecuencias
    bins = 20
    axs[0, 0].hist(datos, bins=bins, edgecolor="white", color="#378ADD")
    axs[0, 0].axhline(n / bins, color="red", linestyle="--", label="Esperado")
    axs[0, 0].set_title("Histograma de frecuencias")
    axs[0, 0].set_xlabel("u(n)")
    axs[0, 0].set_ylabel("Frecuencia")
    axs[0, 0].legend()

    # 2. Diagrama de dispersión u(n) vs u(n+1)
    axs[0, 1].scatter(datos[:-1], datos[1:], s=1, alpha=0.4, color="#378ADD")
    axs[0, 1].set_title("Dispersión: u(n) vs u(n+1)")
    axs[0, 1].set_xlabel("u(n)")
    axs[0, 1].set_ylabel("u(n+1)")

    # 3. Serie temporal (primeros 200 valores)
    axs[1, 0].plot(datos[:200], linewidth=0.6, color="#378ADD")
    axs[1, 0].set_title("Serie temporal (primeros 200 valores)")
    axs[1, 0].set_xlabel("n")
    axs[1, 0].set_ylabel("u(n)")

    # 4. Distribución empírica vs teórica U[0,1)
    sorted_data = np.sort(datos)
    empirical = np.arange(1, n + 1) / n
    axs[1, 1].plot(sorted_data, empirical, label="Empírica", color="#378ADD")
    axs[1, 1].plot([0, 1], [0, 1], "r--", label="U[0,1) teórica")
    axs[1, 1].set_title("Distribución empírica vs teórica (KS)")
    axs[1, 1].set_xlabel("u")
    axs[1, 1].set_ylabel("F(u)")
    axs[1, 1].legend()

    plt.tight_layout()
    nombre_archivo = f"{nombre.lower().replace(' ', '_')}_diagnostico.png"
    plt.savefig(nombre_archivo, dpi=150)
    plt.show()
    print(f"Figura guardada: {nombre_archivo}")



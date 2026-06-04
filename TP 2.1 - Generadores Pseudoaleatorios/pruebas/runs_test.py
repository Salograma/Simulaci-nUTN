"""
Runs Test (Prueba de Rachas)
=============================
Evalúa independencia: clasifica cada valor como sobre o bajo
la mediana y cuenta las rachas. Una cantidad de rachas muy
alta o muy baja indica dependencia entre valores consecutivos.

H0: la secuencia es aleatoria (independiente).
Se rechaza H0 si p_valor < alpha.

Parámetros
datos  : secuencia de valores en [0, 1)
alpha  : nivel de significancia

Retorna
Diccionario con rachas, estadístico Z, p-valor y resultado.
"""

import math
import numpy as np
from scipy import stats


def prueba_runs(datos: list[float], alpha: float = 0.05) -> dict:

    mediana = np.median(datos)
    binario = [1 if v >= mediana else 0 for v in datos]

    n = len(binario)
    n1 = sum(binario)
    n2 = n - n1

    rachas = 1
    for i in range(1, n):
        if binario[i] != binario[i - 1]:
            rachas += 1

    mu_r = (2 * n1 * n2) / n + 1
    sigma2_r = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))

    z = (rachas - mu_r) / math.sqrt(sigma2_r)
    p_valor = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        "prueba": "Runs Test",
        "rachas_observadas": rachas,
        "rachas_esperadas": round(mu_r, 4),
        "estadistico_Z": round(z, 4),
        "p_valor": round(p_valor, 4),
        "alpha": alpha,
        "resultado": "Aprobada" if p_valor > alpha else "Rechazada",
    }

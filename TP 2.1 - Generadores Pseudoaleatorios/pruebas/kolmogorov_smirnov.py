"""
Prueba de Kolmogorov-Smirnov (KS)
===================================
Evalúa ajuste: compara la función de distribución empírica
con la teórica U[0,1) usando el estadístico:

    D = max|F_n(x) - F(x)|

Valor crítico aproximado para alpha=0.05: 1.36 / sqrt(n)

H0: los datos provienen de una distribución U[0,1).
Se rechaza H0 si D >= valor crítico.

Parámetros
datos  : secuencia de valores en [0, 1)
alpha  : nivel de significancia (solo soporta 0.05 para valor crítico tabular)

Retorna
Diccionario con estadístico D, valor crítico, p-valor y resultado.
"""

import math
from scipy import stats


def prueba_ks(datos: list[float], alpha: float = 0.05) -> dict:
    n = len(datos)
    d_stat, p_valor = stats.kstest(datos, "uniform")

    # Valor crítico tabular para alpha = 0.05
    critico = 1.36 / math.sqrt(n)

    return {
        "prueba": "Kolmogorov-Smirnov",
        "estadistico_D": round(d_stat, 4),
        "valor_critico": round(critico, 4),
        "p_valor": round(p_valor, 4),
        "alpha": alpha,
        "resultado": "Aprobada" if d_stat < critico else "Rechazada",
    }

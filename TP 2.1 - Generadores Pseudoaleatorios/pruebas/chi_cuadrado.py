"""
Prueba Chi-cuadrado
====================
Evalúa uniformidad: divide [0,1) en k intervalos iguales
y compara frecuencias observadas con la esperada n/k.

H0: los datos siguen una distribución uniforme U[0,1).
Se rechaza H0 si p_valor < alpha.

Parámetros
datos  : secuencia de valores en [0, 1)
k      : número de intervalos (bins)
alpha  : nivel de significancia

Retorna
Diccionario con estadístico, p-valor y resultado.
"""

import numpy as np
from scipy import stats


def prueba_chi_cuadrado(datos: list[float],
                        k: int = 10,
                        alpha: float = 0.05) -> dict:

    n = len(datos)
    observado, _ = np.histogram(datos, bins=k, range=(0, 1))
    esperado = np.full(k, n / k)

    chi2, p_valor = stats.chisquare(f_obs=observado, f_exp=esperado)

    return {
        "prueba": "Chi-cuadrado",
        "estadistico": round(chi2, 4),
        "grados_libertad": k - 1,
        "p_valor": round(p_valor, 4),
        "alpha": alpha,
        "resultado": "Aprobada" if p_valor > alpha else "Rechazada",
        "observado": observado.tolist(),
        "esperado_por_bin": round(n / k, 2),
    }

"""
Evalúa independencia temporal: calcula el coeficiente de
correlación entre la secuencia y ella misma desplazada lag
posiciones. Valores cercanos a 0 indican independencia.

H0: no existe autocorrelación significativa para el lag dado.
Se rechaza H0 si p_valor < alpha.

Parámetros
datos  : secuencia de valores en [0, 1)
lag    : desfase a evaluar (default: 1)
alpha  : nivel de significancia

Retorna
Diccionario con coeficiente r, estadístico Z, p-valor y resultado.
"""

import math
import numpy as np
from scipy import stats


def prueba_autocorrelacion(datos: list[float],
                           lag: int = 1,
                           alpha: float = 0.05) -> dict:

    arr = np.array(datos)
    n = len(arr)

    r = np.corrcoef(arr[:-lag], arr[lag:])[0, 1]

    z = r * math.sqrt(n - lag)
    p_valor = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        "prueba": f"Autocorrelación (lag={lag})",
        "coeficiente_r": round(r, 4),
        "estadistico_Z": round(z, 4),
        "p_valor": round(p_valor, 4),
        "alpha": alpha,
        "resultado": "Aprobada" if p_valor > alpha else "Rechazada",
    }

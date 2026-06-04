"""
Punto de entrada del TP. Ejecuta el GCL y el ITA, corre las 4 pruebas
sobre cada uno y genera los gráficos de diagnóstico.
"""

import numpy as np
import random

from generadores.gcl import gcl
from generadores.ita import ita
from graficos import graficar
from pruebas import (
    prueba_chi_cuadrado,
    prueba_runs,
    prueba_ks,
    prueba_autocorrelacion,
)

# Parametros
N = 10_000

GENERADORES = {
    "GCL": gcl(semilla=12345, n=N),
    "ITA": ita(s0=4120, s1=1300, s2=490, n=N),
    "Python random": [random.random() for _ in range(N)],
}

PRUEBAS = [
    prueba_chi_cuadrado,
    prueba_runs,
    prueba_ks,
    prueba_autocorrelacion,
]

# Ejecucion
for nombre, datos in GENERADORES.items():

    print("=" * 50)
    print(f" {nombre} — Resumen estadístico")
    print("=" * 50)
    print(f"  N        : {N}")
    print(f"  Media    : {np.mean(datos):.4f}  (esperado ≈ 0.5000)")
    print(f"  Desvío   : {np.std(datos):.4f}  (esperado ≈ 0.2887)")
    print(f"  Mínimo   : {min(datos):.4f}")
    print(f"  Máximo   : {max(datos):.4f}")

    print("\n── Pruebas de calidad ──\n")
    for funcion in PRUEBAS:
        p = funcion(datos)
        estado = "✓" if p["resultado"] == "Aprobada" else "✗"
        print(f"  [{estado}] {p['prueba']}")
        for k, v in p.items():
            if k not in ("prueba", "resultado", "observado"):
                print(f"       {k}: {v}")
        print()

    graficar(datos, nombre=nombre)

# Tabla
print("\n── Tabla comparativa ──\n")
import comparacion

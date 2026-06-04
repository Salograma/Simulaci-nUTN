"""
Ejecuta todas las pruebas estadísticas sobre cada generador y presenta los resultados en una tabla comparativa.
"""

import random
import numpy as np

from generadores.gcl import gcl
from generadores.ita import ita
from pruebas import (
    prueba_chi_cuadrado,
    prueba_runs,
    prueba_ks,
    prueba_autocorrelacion,
)

# Parametros
N = 10_000

generadores = {
    "GCL":          gcl(semilla=12345, n=N),
    "ITA":          ita(s0=4120, s1=1300, s2=490, n=N),
    "Python random": [random.random() for _ in range(N)],
}

PRUEBAS = [
    ("Chi-cuadrado",       prueba_chi_cuadrado),
    ("Runs Test",          prueba_runs),
    ("Kolmogorov-Smirnov", prueba_ks),
    ("Autocorrelación",    prueba_autocorrelacion),
]

# Tabla
COL = 18

def separador():
    print("─" * (22 + COL * len(generadores)))

print(f"\n{'Prueba':<22}", end="")
for nombre in generadores:
    print(f"{nombre:^{COL}}", end="")
print()
separador()

for nombre_prueba, funcion in PRUEBAS:
    print(f"{'  ' + nombre_prueba + ' (p)':<22}", end="")
    for datos in generadores.values():
        res = funcion(datos)
        p = res.get("p_valor", res.get("estadistico_D", "—"))
        print(f"{str(p):^{COL}}", end="")
    print()

    print(f"{'  resultado':<22}", end="")
    for datos in generadores.values():
        res = funcion(datos)
        print(f"{res['resultado']:^{COL}}", end="")
    print()
    separador()

print("\nNota: 'Aprobada' indica que no hay evidencia para rechazar H0 (p > 0.05).\n")

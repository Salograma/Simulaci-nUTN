"""
Generador Congruencial Lineal (GCL)
====================================
Fórmula: X(n+1) = (a * X(n) + c) mod m
         u(n)   = X(n) / m          ∈ [0, 1)

Parámetros por defecto (Numerical Recipes):
    a = 1_664_525
    c = 1_013_904_223
    m = 2**32
"""


def gcl(semilla: int, n: int,
        a: int = 1_664_525,
        c: int = 1_013_904_223,
        m: int = 2**32) -> list[float]:
    numeros = []
    x = semilla
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros

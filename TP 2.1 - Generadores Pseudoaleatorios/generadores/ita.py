"""
Generador Itamaracá (ITA) — versión simplificada
==================================================
Referencia: Pereira, D.H. "Itamaracá: A Novel Simple Way to Generate
Pseudo-Random Numbers."

Algoritmo (versión simplificada):
    Paso 1 — Pn (n Process):
        Pn = |S2 - S0|

    Paso 2 — Cálculo final:
        FRNSn = |N - (Pn * Xrn)|

    Donde:
        S0, S1, S2 : tres semillas en el rango [1, N]
        N          : valor máximo del rango (entero natural)
        Xrn        : constante racional fija cercana a 2 (elegida arbitrariamente)
        FRNSn      : siguiente valor generado, también en [1, N]

    Las semillas se desplazan en cada iteración:
        S0 ← S1
        S1 ← S2
        S2 ← FRNSn

Normalización:
    Para compatibilidad con las pruebas estadísticas (que esperan [0, 1))
    se divide cada valor generado por N: u(n) = FRNSn / N
"""


def ita(s0: int, s1: int, s2: int, n: int,
        xrn: float = 1.9,
        normalizar: bool = True) -> list[float]:
    if not (1 <= s0 <= n and 1 <= s1 <= n and 1 <= s2 <= n):
        raise ValueError(f"Las semillas deben estar en el rango [1, {n}].")

    numeros = []
    a, b, c = s0, s1, s2

    for _ in range(n):
        pn = abs(c - a)                    # Paso 1: Pn = |S2 - S0|
        frns = abs(n - (pn * xrn))         # Paso 2: FRNSn = |N - Pn * Xrn|
        frns = max(1, min(n, round(frns))) # Clamp a [1, N]

        numeros.append(frns / n if normalizar else frns)

        # Desplazamiento de semillas
        a, b, c = b, c, frns

    return numeros

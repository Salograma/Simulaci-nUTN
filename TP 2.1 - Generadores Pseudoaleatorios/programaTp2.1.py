"""
Simulador de Generadores Pseudoaleatorios - PROYECTO UNIFICADO

Este script integra en un único archivo:
- Generadores pseudoaleatorios (GCL, ITA, Python random)
- Pruebas estadísticas (Chi-cuadrado, Runs, KS, Autocorrelación)
- Gráficos diagnósticos y tabla comparativa

Requisitos: pip install numpy scipy matplotlib
Uso: python simulador_pseudoaleatorio.py
"""

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from scipy import stats


# ============================================================================
# GENERADORES PSEUDOALEATORIOS
# ============================================================================

def gcl(semilla: int, n: int,
        a: int = 1_664_525,
        c: int = 1_013_904_223,
        m: int = 2**32) -> list[float]:
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
    numeros = []
    x = semilla
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros


def ita(s0: int, s1: int, s2: int, n: int,
        xrn: float = 1.9,
        normalizar: bool = True) -> list[float]:
    """
    Generador Itamaracá (ITA) — versión simplificada
    ==================================================
    Algoritmo:
        Paso 1 — Pn (n Process): Pn = |S2 - S0|
        Paso 2 — Cálculo final: FRNSn = |N - (Pn * Xrn)|
    
    Normalización: u(n) = FRNSn / N
    """
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


# ============================================================================
# PRUEBAS ESTADÍSTICAS
# ============================================================================

def prueba_chi_cuadrado(datos: list[float],
                        k: int = 10,
                        alpha: float = 0.05) -> dict:
    """
    Prueba Chi-cuadrado
    ====================
    Evalúa uniformidad: divide [0,1) en k intervalos y compara
    frecuencias observadas con la esperada n/k.
    
    H0: los datos siguen una distribución uniforme U[0,1).
    Se rechaza H0 si p_valor < alpha.
    """
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


def prueba_runs(datos: list[float], alpha: float = 0.05) -> dict:
    """
    Runs Test (Prueba de Rachas)
    =============================
    Evalúa independencia: clasifica cada valor como sobre o bajo
    la mediana y cuenta las rachas. Una cantidad de rachas muy
    alta o muy baja indica dependencia entre valores consecutivos.
    
    H0: la secuencia es aleatoria (independiente).
    Se rechaza H0 si p_valor < alpha.
    """
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


def prueba_ks(datos: list[float], alpha: float = 0.05) -> dict:
    """
    Prueba de Kolmogorov-Smirnov (KS)
    ===================================
    Evalúa ajuste: compara la función de distribución empírica
    con la teórica U[0,1) usando el estadístico D = max|F_n(x) - F(x)|
    
    H0: los datos provienen de una distribución U[0,1).
    Se rechaza H0 si D >= valor crítico.
    """
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


def prueba_autocorrelacion(datos: list[float],
                           lag: int = 1,
                           alpha: float = 0.05) -> dict:
    """
    Autocorrelación
    ===============
    Evalúa independencia temporal: calcula el coeficiente de
    correlación entre la secuencia y ella misma desplazada lag
    posiciones. Valores cercanos a 0 indican independencia.
    
    H0: no existe autocorrelación significativa para el lag dado.
    Se rechaza H0 si p_valor < alpha.
    """
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


# ============================================================================
# GRÁFICOS DIAGNÓSTICOS
# ============================================================================

def graficar(datos: list[float], nombre: str = "Generador") -> None:
    """
    Función genérica de diagnóstico visual para generadores pseudoaleatorios.
    Aplicable a cualquier secuencia de valores en [0, 1).
    
    Gráficos generados:
        1. Histograma de frecuencias
        2. Diagrama de dispersión u(n) vs u(n+1)
        3. Serie temporal (primeros 200 valores)
        4. Distribución empírica vs teórica U[0,1) (KS)
    """
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


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
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
    
    # Tabla comparativa
    print("\n" + "=" * 50)
    print(" Tabla Comparativa")
    print("=" * 50)
    
    COL = 18
    
    def separador():
        print("─" * (22 + COL * len(GENERADORES)))
    
    print(f"\n{'Prueba':<22}", end="")
    for nombre in GENERADORES:
        print(f"{nombre:^{COL}}", end="")
    print()
    separador()
    
    for funcion in PRUEBAS:
        nombre_prueba = funcion.__name__.replace("prueba_", "").replace("_", " ").title()
        if nombre_prueba == "Chi Cuadrado":
            nombre_prueba = "Chi-cuadrado"
        elif nombre_prueba == "Ks":
            nombre_prueba = "Kolmogorov-Smirnov"
        elif nombre_prueba == "Autocorrelacion":
            nombre_prueba = "Autocorrelación"
        elif nombre_prueba == "Runs":
            nombre_prueba = "Runs Test"
        
        print(f"{'  ' + nombre_prueba + ' (p)':<22}", end="")
        for datos in GENERADORES.values():
            res = funcion(datos)
            p = res.get("p_valor", res.get("estadistico_D", "—"))
            print(f"{str(p):^{COL}}", end="")
        print()
        
        print(f"{'  resultado':<22}", end="")
        for datos in GENERADORES.values():
            res = funcion(datos)
            print(f"{res['resultado']:^{COL}}", end="")
        print()
        separador()
    
    print("\nNota: 'Aprobada' indica que no hay evidencia para rechazar H0 (p > 0.05).\n")


if __name__ == "__main__":
    main()
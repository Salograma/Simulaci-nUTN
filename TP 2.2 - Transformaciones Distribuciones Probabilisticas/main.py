"""
Generadores de distribuciones de probabilidad a partir de uniformes U(0,1).
Todas las distribuciones se generan usando transformada inversa sobre el GCL.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from generadores.gcl import gcl

# ─── Generador base ───────────────────────────────────────────────────────────

N = 10_000
SEMILLA = 12345

def get_uniformes(n=N):
    return gcl(semilla=SEMILLA, n=n)

# ─── Transformaciones ─────────────────────────────────────────────────────────

def gen_uniforme(a, b, uniformes):
    """Transformada inversa: X = a + (b - a) * r"""
    return [a + (b - a) * u for u in uniformes]

def gen_exponencial(lam, uniformes):
    """Transformada inversa: X = -ln(r) / lambda"""
    return [-math.log(u) / lam for u in uniformes]

def gen_normal(mu, sigma, uniformes):
    """Box-Muller: usa pares de uniformes"""
    muestras = []
    it = iter(uniformes)
    for r1 in it:
        r2 = next(it, None)
        if r2 is None:
            break
        if r1 == 0:
            r1 = 1e-10
        z = math.sqrt(-2 * math.log(r1)) * math.cos(2 * math.pi * r2)
        muestras.append(mu + z * sigma)
    return muestras

def gen_binomial(n_ensayos, p, uniformes):
    """Transformada inversa discreta: acumula P(X=k) hasta superar r"""
    muestras = []
    for r in uniformes:
        acum = 0.0
        for k in range(n_ensayos + 1):
            acum += math.comb(n_ensayos, k) * (p ** k) * ((1 - p) ** (n_ensayos - k))
            if r <= acum:
                muestras.append(k)
                break
    return muestras

def gen_poisson(lam, uniformes):
    """Transformada inversa discreta: acumula P(X=k) hasta superar r"""
    muestras = []
    for r in uniformes:
        acum = 0.0
        k = 0
        while True:
            acum += math.exp(-lam) * (lam ** k) / math.factorial(k)
            if r <= acum:
                muestras.append(k)
                break
            k += 1
    return muestras

def gen_empirica_discreta(valores, probabilidades, uniformes):
    """
    Transformada inversa para distribución empírica discreta.
    valores: lista de valores posibles
    probabilidades: lista de probabilidades correspondientes (deben sumar 1)
    """
    acumuladas = []
    acum = 0.0
    for p in probabilidades:
        acum += p
        acumuladas.append(acum)

    muestras = []
    for r in uniformes:
        for i, fa in enumerate(acumuladas):
            if r <= fa:
                muestras.append(valores[i])
                break
    return muestras

# ─── Testeo ───────────────────────────────────────────────────────────────────

def _convergencia(muestras, esperanza_teo, varianza_teo, nombre, archivo):
    N = len(muestras)
    cuadrados = [x**2 for x in muestras]

    esperanza_n = []
    esperanza_cuad_n = []

    for i in range(N):
        if i == 0:
            esperanza_n.append(muestras[0])
            esperanza_cuad_n.append(cuadrados[0])
        else:
            esperanza_n.append((esperanza_n[i-1] * i + muestras[i]) / (i + 1))
            esperanza_cuad_n.append((esperanza_cuad_n[i-1] * i + cuadrados[i]) / (i + 1))

    varianza_n = [esperanza_cuad_n[i] - esperanza_n[i]**2 for i in range(N)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(f'Convergencia — {nombre}')

    axes[0].plot(esperanza_n, label='E[X] muestral', alpha=0.8)
    axes[0].axhline(esperanza_teo, color='r', linestyle='--', label=f'E[X] teórica = {esperanza_teo:.4f}')
    axes[0].set_title('Esperanza')
    axes[0].legend()

    axes[1].plot(varianza_n, label='Var[X] muestral', alpha=0.8)
    axes[1].axhline(varianza_teo, color='r', linestyle='--', label=f'Var[X] teórica = {varianza_teo:.4f}')
    axes[1].set_title('Varianza')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(archivo)
    plt.show()


def _chi_continua(muestras, dist_scipy, params_scipy, nombre, archivo, k=20):
    """Chi-cuadrado para distribuciones continuas usando intervalos equiprobables."""
    n = len(muestras)
    limites = [dist_scipy.ppf(i / k, **params_scipy) for i in range(k + 1)]
    limites[-1] = np.inf

    observadas, _ = np.histogram(muestras, bins=limites)
    esperadas = np.full(k, n / k)
    chi2, p_valor = stats.chisquare(observadas, esperadas)

    _tabla_chi(
        intervalos=[f'[{limites[i]:.2f}, {limites[i+1]:.2f})' for i in range(k)],
        observadas=observadas,
        esperadas=esperadas,
        chi2=chi2, p_valor=p_valor,
        nombre=nombre, archivo=archivo, n=n, k=k
    )


def _chi_discreta(muestras, valores_posibles, probs_teoricas, nombre, archivo):
    n = len(muestras)
    observadas = np.array([muestras.count(v) for v in valores_posibles], dtype=float)
    esperadas = np.array([p * n for p in probs_teoricas], dtype=float)

    # Agrupar colas con esperada < 5
    grupos_obs, grupos_esp, etiquetas = [], [], []
    buf_obs, buf_esp = 0.0, 0.0
    inicio = None

    for i, (o, e, v) in enumerate(zip(observadas, esperadas, valores_posibles)):
        if e < 5:
            buf_obs += o
            buf_esp += e
            if inicio is None:
                inicio = v
        else:
            if buf_esp > 0:
                grupos_obs.append(buf_obs)
                grupos_esp.append(buf_esp)
                etiquetas.append(f'≤{v-1}')
                buf_obs, buf_esp, inicio = 0.0, 0.0, None
            grupos_obs.append(o)
            grupos_esp.append(e)
            etiquetas.append(str(v))

    # Volcar buffer restante
    if buf_esp > 0:
        grupos_obs.append(buf_obs)
        grupos_esp.append(buf_esp)
        etiquetas.append(f'≥{inicio}')

    grupos_obs = np.array(grupos_obs, dtype=float)
    grupos_esp = np.array(grupos_esp, dtype=float)

    # Normalizar para evitar error de precisión numérica
    grupos_esp = grupos_esp * (grupos_obs.sum() / grupos_esp.sum())

    chi2, p_valor = stats.chisquare(grupos_obs, grupos_esp)

    _tabla_chi(
        intervalos=etiquetas,
        observadas=grupos_obs,
        esperadas=grupos_esp,
        chi2=chi2, p_valor=p_valor,
        nombre=nombre, archivo=archivo,
        n=n, k=len(grupos_obs)
    )


def _tabla_chi(intervalos, observadas, esperadas, chi2, p_valor, nombre, archivo, n, k):
    fig, ax = plt.subplots(figsize=(9, max(4, len(intervalos) * 0.35 + 1.5)))
    ax.axis('off')

    filas = []
    for etq, o, e in zip(intervalos, observadas, esperadas):
        contrib = (o - e)**2 / e if e > 0 else 0
        filas.append([etq, str(int(o)), f'{e:.1f}', f'{contrib:.4f}'])

    tabla = ax.table(
        cellText=filas,
        colLabels=['Intervalo/Valor', 'Observadas', 'Esperadas', '(O-E)²/E'],
        loc='center', cellLoc='center',
        bbox=[0, 0, 1, 0.92]
    )
    tabla.scale(1, 1.4)

    resultado = 'Aprobada ✓' if p_valor > 0.05 else 'Rechazada ✗'
    ax.set_title(
        f'Prueba χ² — {nombre}\nχ² = {chi2:.4f}  |  p-valor = {p_valor:.4f}  |  {resultado}  |  N = {n}  |  clases = {k}',
        pad=10, fontsize=10
    )

    plt.tight_layout()
    plt.savefig(archivo)
    plt.show()


def _histograma_continuo(muestras, x_teo, y_teo, nombre, archivo):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(muestras, bins=50, density=True, alpha=0.7, label='Muestras')
    ax.plot(x_teo, y_teo, 'r-', label='Teórica')
    ax.set_title(f'Histograma — {nombre}')
    ax.legend()
    plt.tight_layout()
    plt.savefig(archivo)
    plt.show()


def _histograma_discreto(muestras, valores, probs_teo, nombre, archivo):
    n = len(muestras)
    frec_obs = [muestras.count(v) / n for v in valores]
    x = np.array(valores)

    fig, ax = plt.subplots(figsize=(8, 4))
    ancho = 0.35
    ax.bar(x - ancho/2, frec_obs, width=ancho, alpha=0.7, label='Observada')
    ax.bar(x + ancho/2, probs_teo, width=ancho, alpha=0.7, color='r', label='Teórica')
    ax.set_title(f'Frecuencias relativas — {nombre}')
    ax.legend()
    plt.tight_layout()
    plt.savefig(archivo)
    plt.show()


# ─── Testeos por distribución ─────────────────────────────────────────────────

def testear_uniforme(a=0, b=1):
    u = get_uniformes()
    muestras = gen_uniforme(a, b, u)

    esp_teo = (a + b) / 2
    var_teo = (b - a)**2 / 12

    x = np.linspace(a, b, 200)
    _histograma_continuo(muestras, x, np.full_like(x, 1/(b-a)), 'Uniforme', 'hist_uniforme.png')
    _convergencia(muestras, esp_teo, var_teo, 'Uniforme', 'conv_uniforme.png')
    _chi_continua(muestras, stats.uniform, {'loc': a, 'scale': b - a}, 'Uniforme', 'chi2_uniforme.png')


def testear_exponencial(lam=2):
    u = get_uniformes()
    muestras = gen_exponencial(lam, u)

    esp_teo = 1 / lam
    var_teo = 1 / lam**2

    x = np.linspace(0, max(muestras), 200)
    _histograma_continuo(muestras, x, lam * np.exp(-lam * x), 'Exponencial', 'hist_exponencial.png')
    _convergencia(muestras, esp_teo, var_teo, 'Exponencial', 'conv_exponencial.png')
    _chi_continua(muestras, stats.expon, {'scale': 1/lam}, 'Exponencial', 'chi2_exponencial.png')


def testear_normal(mu=0, sigma=1):
    u = get_uniformes(N * 2)  # Box-Muller consume pares
    muestras = gen_normal(mu, sigma, u)

    esp_teo = mu
    var_teo = sigma**2

    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
    _histograma_continuo(muestras, x, stats.norm.pdf(x, mu, sigma), 'Normal', 'hist_normal.png')
    _convergencia(muestras, esp_teo, var_teo, 'Normal', 'conv_normal.png')
    _chi_continua(muestras, stats.norm, {'loc': mu, 'scale': sigma}, 'Normal', 'chi2_normal.png')


def testear_binomial(n_ensayos=20, p=0.4):
    u = get_uniformes()
    muestras = gen_binomial(n_ensayos, p, u)

    esp_teo = n_ensayos * p
    var_teo = n_ensayos * p * (1 - p)

    valores = list(range(n_ensayos + 1))
    probs_teo = [math.comb(n_ensayos, k) * p**k * (1-p)**(n_ensayos-k) for k in valores]

    _histograma_discreto(muestras, valores, probs_teo, 'Binomial', 'hist_binomial.png')
    _convergencia(muestras, esp_teo, var_teo, 'Binomial', 'conv_binomial.png')
    _chi_discreta(muestras, valores, probs_teo, 'Binomial', 'chi2_binomial.png')


def testear_poisson(lam=3):
    u = get_uniformes()
    muestras = gen_poisson(lam, u)

    esp_teo = lam
    var_teo = lam

    k_max = int(lam + 4 * math.sqrt(lam)) + 1
    valores = list(range(k_max + 1))
    probs_teo = [math.exp(-lam) * lam**k / math.factorial(k) for k in valores]

    _histograma_discreto(muestras, valores, probs_teo, 'Poisson', 'hist_poisson.png')
    _convergencia(muestras, esp_teo, var_teo, 'Poisson', 'conv_poisson.png')
    _chi_discreta(muestras, valores, probs_teo, 'Poisson', 'chi2_poisson.png')


def testear_empirica_discreta():
    # Ejemplo: demanda de un producto con distribución conocida
    valores = [0, 1, 2, 3, 4, 5]
    probabilidades = [0.10, 0.20, 0.30, 0.25, 0.10, 0.05]

    u = get_uniformes()
    muestras = gen_empirica_discreta(valores, probabilidades, u)

    esp_teo = sum(v * p for v, p in zip(valores, probabilidades))
    esp_cuad_teo = sum(v**2 * p for v, p in zip(valores, probabilidades))
    var_teo = esp_cuad_teo - esp_teo**2

    _histograma_discreto(muestras, valores, probabilidades, 'Empírica Discreta', 'hist_empirica.png')
    _convergencia(muestras, esp_teo, var_teo, 'Empírica Discreta', 'conv_empirica.png')
    _chi_discreta(muestras, valores, probabilidades, 'Empírica Discreta', 'chi2_empirica.png')


# ─── Main con selección por consola ───────────────────────────────────────────

OPCIONES = {
    '1': ('Uniforme',           testear_uniforme),
    '2': ('Exponencial',        testear_exponencial),
    '3': ('Normal',             testear_normal),
    '4': ('Binomial',           testear_binomial),
    '5': ('Poisson',            testear_poisson),
    '6': ('Empírica Discreta',  testear_empirica_discreta),
    '7': ('Todas',              None),
}

if __name__ == '__main__':
    print("\n── Generador de distribuciones ──\n")
    for k, (nombre, _) in OPCIONES.items():
        print(f"  {k}. {nombre}")

    opcion = input("\nElegí una opción: ").strip()

    if opcion == '7':
        for k, (nombre, fn) in OPCIONES.items():
            if fn is not None:
                print(f"\nGenerando {nombre}...")
                fn()
    elif opcion in OPCIONES:
        nombre, fn = OPCIONES[opcion]
        print(f"\nGenerando {nombre}...")
        fn()
    else:
        print("Opción inválida.")
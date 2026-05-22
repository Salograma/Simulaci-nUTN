import random
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

opcionesS = ['m', 'd', 'f', 'o']
opcionesA = ['i', 'f']

nombres_estrategias = {
    'm': 'Martingala',
    'd': "D'Alembert",
    'f': 'Fibonacci',
    'o': 'Otra (Óptima)'
}

def graficar(historial_corridas, quiebras, estrategia, capital, tiradasPorCorrida):
    nombre = nombres_estrategias.get(estrategia, estrategia)
    tipo_capital = "Infinito" if capital == 'i' else "Finito"
    capital_inicial = 0 if capital == 'i' else 500
 
    # --- Preparar matriz igualando longitudes al mínimo ---
    min_len = min(len(h) for h in historial_corridas)
    matriz = np.array([h[:min_len] for h in historial_corridas], dtype=float)
    tiradas = np.arange(1, min_len + 1)
    promedio = matriz.mean(axis=0)
 
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Estrategia: {nombre} | Capital: {tipo_capital}", fontsize=14, fontweight='bold')
 
    # ── Gráfica 1: Flujo de caja de cada corrida ──────────────────────────────
    ax1 = axes[0, 0]
    for h in historial_corridas:
        ax1.plot(range(1, len(h) + 1), h, alpha=0.3, linewidth=0.8, color='red')
    ax1.axhline(y=capital_inicial, color='blue', linestyle='--', linewidth=1.5, label='Capital inicial (fci)')
    ax1.set_title('Flujo de caja por corrida')
    ax1.set_xlabel('Tirada (n)')
    ax1.set_ylabel('Capital ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
 
    # ── Gráfica 2: Flujo de caja promedio ─────────────────────────────────────
    ax2 = axes[0, 1]
    ax2.plot(tiradas, promedio, color='red', linewidth=2, label='fc (promedio)')
    ax2.axhline(y=capital_inicial, color='blue', linestyle='--', linewidth=1.5, label='fci (capital inicial)')
    ax2.set_title('Flujo de caja promedio')
    ax2.set_xlabel('Tirada (n)')
    ax2.set_ylabel('Capital promedio ($)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
 
    # ── Gráfica 3: Frecuencia relativa de éxito por tirada (frsa) ─────────────
    ax3 = axes[1, 0]
    frsa = [
        np.sum(matriz[:, n] > capital_inicial) / len(historial_corridas)
        for n in range(min_len)
    ]
    ax3.bar(tiradas, frsa, color='red', alpha=0.7, width=1.0)
    ax3.axhline(y=0.5, color='black', linestyle='--', linewidth=1.2, label='50%')
    # Línea de probabilidad teórica de ganar apostando al rojo: 18/37
    ax3.axhline(y=18/37, color='green', linestyle=':', linewidth=1.2, label='P teórica (18/37 ≈ 0.486)')
    ax3.set_title('Frecuencia relativa de éxito por tirada (frsa)')
    ax3.set_xlabel('Tirada (n)')
    ax3.set_ylabel('frsa')
    ax3.set_ylim(0, 1)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
 
    # ── Gráfica 4: Quiebras (solo capital finito) ──────────────────────────────
    ax4 = axes[1, 1]
    if capital == 'f':
        quiebras_por_corrida = []
        for h in historial_corridas:
            # Si la corrida terminó antes de las tiradas pedidas, quebró
            quiebras_por_corrida.append(1 if len(h) < tiradasPorCorrida else 0)
        acumulado = np.cumsum(quiebras_por_corrida)
        ax4.step(range(1, len(acumulado) + 1), acumulado, color='darkred', linewidth=2)
        ax4.set_title(f'Quiebras acumuladas (total: {quiebras})')
        ax4.set_xlabel('Corrida')
        ax4.set_ylabel('Quiebras acumuladas')
        ax4.grid(True, alpha=0.3)
    else:
        ax4.text(0.5, 0.5, 'No aplica\n(capital infinito)',
                 ha='center', va='center', fontsize=13, color='gray',
                 transform=ax4.transAxes)
        ax4.set_title('Quiebras')
        ax4.axis('off')
 
    plt.tight_layout()
    plt.savefig(f'resultado_{estrategia}_{capital}.png', dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Gráfica guardada como: resultado_{estrategia}_{capital}.png")



def parse_args():
    parser = argparse.ArgumentParser(description='Simulador de ruleta')
    parser.add_argument('-c', type=int, default=1,   help='Cantidad de corridas')
    parser.add_argument('-n', type=int, default=100, help='Tiradas por corrida')
    ###parser.add_argument('-e', type=int, default=7,   help='Número elegido (0-36)')
    parser.add_argument('-s', type=str, required=True, choices=opcionesS,
                        help='Estrategia: m=Martingala, d=DAlembert, f=Fibonacci, o=Otra')
    parser.add_argument('-a', type=str, required=True, choices=opcionesA,
                        help='Tipo de capital: i=infinito, f=finito')
    return parser.parse_args()



def validar_argumentos(args):
    errores = []

    if args.c <= 0:
        errores.append(f"Las corridas (-c) deben ser mayor a 0. Recibido: {args.c}")

    if args.n <= 0:
        errores.append(f"Las tiradas (-n) deben ser mayor a 0. Recibido: {args.n}")

    if args.s not in opcionesS:
        errores.append(f"La estrategia utilizada no existe. Debe ser 'm', 'd', 'f' u 'o'. Recibido: {args.s}")
    
    if args.a not in opcionesA:
        errores.append(f"No eligió un capital válido. Debe ser o bieen, infinito: 'i' o finito: 'f'. Recibido: {args.a}")

    if errores:
        for e in errores:
            print(f"[ERROR] {e}")
        sys.exit(1)

fib = [0] * 100
fib[0] = 1
fib[1] = 1
for i in range(2,100):
    fib[i] = fib[i-1] + fib[i-2]

print("Simulador de ruleta")

red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

def tirada():
    return random.randint(0, 36)

def frecuenciaRelativa(xi, n):
    return round(xi / n, 2)

# Valores esperados
fre = 1 / 37                                       # 0.027 (frecuencia relativa esperada)
vpe = sum(range(37)) / 37                         # 18.0 (valor promedio esperado)
vve = sum((x - vpe)**2 for x in range(37)) / 37  # ≈  114.5 (valor de la varianza de esperada)
vde = vve ** 0.5                                  # ≈ 10.7(valor del desvio esperado)

## ------------------------ MARTINGALA

def martingala(tiradas, capitalArg):
    capital = None if capitalArg == 'i' else 500
    apuesta_base = 1
    apuesta = apuesta_base

    historial_capital = []

    red = [1, 3, 5, 7, 9, 12, 14, 16, 18,
           19, 21, 23, 25, 27, 30, 32, 34, 36]

    color_apuesta = 'rojo'

    capital_infinito = capital is None

    # Si el capital es infinito usamos un valor auxiliar
    if capital_infinito:
        capital_actual = 0
    else:
        capital_actual = capital

    quebrado = False

    for i in range(tiradas):

        # Verificar si puede realizar la apuesta
        if not capital_infinito and apuesta > capital_actual:
            quebrado = True
            break

        # Realiza la apuesta
        capital_actual -= apuesta

        # Tirada de ruleta
        num = random.randint(0, 36)

        # Determinar color
        if num in red:
            color = 'rojo'
        elif num == 0:
            color = 'verde'
        else:
            color = 'negro'

        # Resolver apuesta
        if color == color_apuesta:
            # Gana
            capital_actual += apuesta * 2

            # Reinicia apuesta
            apuesta = apuesta_base
        else:
            # Pierde -> duplica
            apuesta *= 2

        # Guardar historial
        historial_capital.append(capital_actual)

    return historial_capital, quebrado
    

## ------------------------ D'Alembert

def dalembert(tiradas, capitalArg):
    apuesta_base = 10
    apuesta_actual = apuesta_base
    quebro = False
    historial_tiradas = []
    capital_actual = 0 if capitalArg == 'i' else 500
    for i in range(tiradas):
        # 1. Girar la ruleta
        numero = random.randint(0, 36)
        gano = numero != 0 and numero % 2 == 0  # apuesta a números pares

        # 2. Actualizar capital 
        if gano:
            capital_actual += apuesta_actual
        else:
            capital_actual -= apuesta_actual

        # 3. Actualizar apuesta según D'Alembert
        if gano:
            apuesta_actual = max(apuesta_base, apuesta_actual - apuesta_base)
        else:
            apuesta_actual += apuesta_base

        # 4. Guardar estado
        historial_tiradas.append(capital_actual)

        # 5. Condiciones de corte
        if capitalArg == 'f' and capital_actual <= 0:
            quebro = True
            break

    return historial_tiradas, quebro

## ------------------------ FIBONACCI

def reinicio(capital, apuesta, idx):
    capital += apuesta
    apuesta = 5
    idx = 0
    return capital, apuesta, idx


def fibonacci(tiradasPorCorrida, capitalArg):
    if capitalArg == 'f':
        capital = 500
        idx = 0
        apuesta = fib[idx] * 5
        historial = []
        estaQuebrado = False
        for _ in range(tiradasPorCorrida):
            if tirada() in red:
                capital, apuesta, idx = reinicio(capital, apuesta, idx)
                historial.append(capital)
            else:
                capital -= apuesta
                idx += 1
                apuesta = min(capital, 5*fib[idx])
                if apuesta == 0:
                    estaQuebrado = True
                    break
                historial.append(capital)
    else:
        capital = 0
        idx = 0
        apuesta = fib[idx] * 5
        historial = []
        estaQuebrado = False
        for _ in range(tiradasPorCorrida):
            if tirada() not in red:
                capital, apuesta, idx = reinicio(capital, apuesta, idx)
                historial.append(capital)
            else:
                capital -= apuesta
                idx += 1
                apuesta = 5 * fib[idx]
                historial.append(capital)
            
    return historial, estaQuebrado

## ------------------------ OTRA ESTRATEGIA PROPUESTA

def estrategia_optima(ultimasJugadas):
    retornos = ["r", "par", "inf", "filaInf"]
    jugada = ultimasJugadas[-1]
    retornos[0] = "b" if jugada in red else "r"
    retornos[1] = "par" if jugada % 2 == 1 else "impar"
    boolsPierna = [False, False, False]
    boolsFilas = [False, False, False]
    mapPiernas = {0:"inf",1:"med",2:"sup"}
    mapFilas = {0:"filaMed",1:"filaInf",2:"filaSup"}
    for jugada in ultimasJugadas:
        if(boolsFilas.count(True) < 2):
            if jugada == 0:
                continue
            if jugada % 3 == 0:
                boolsFilas[2] = True
            elif jugada % 3 == 1:
                boolsFilas[1] = True
            else:
                boolsFilas[0] = True
        if(boolsPierna.count(True) < 2):
            if jugada == 0:
                continue
            if jugada <= 12:
                boolsPierna[2] = True
            elif jugada <= 24:
                boolsPierna[1] = True
            else:
                boolsPierna[0] = True
        if boolsFilas.count(True) == 2 and boolsPierna.count(True) == 2:
            break
    if boolsFilas.count(True) == 2:
        retornos[3] = mapFilas[boolsFilas.index(False)]
    else:
        retornos[3] = mapFilas[random.randint(0,2)]
    if boolsPierna.count(True) == 2:
        retornos[2] = mapPiernas[boolsPierna.index(False)]
    else:
        retornos[2] = mapPiernas[random.randint(0,2)]
    return retornos
        
def evaluarTirada(numero, apuestaRealizada, base12, base13):
    ganancia = 0
    if numero == 0:
        return 0
    if apuestaRealizada[0] == 'r':
        if numero in red:
            ganancia += 2*base12
    else:
        if numero not in red:
            ganancia += 2*base12
    if apuestaRealizada[1] == 'par':
        if numero % 2 == 0:
            ganancia += 2*base12
    else:
        if numero % 2 == 1:
            ganancia += 2*base12
    if apuestaRealizada[2] == 'inf':
        if numero <= 12 and numero != 0:
            ganancia += 3*base13
    elif apuestaRealizada[2] == 'med':
        if 13 <= numero <= 24:
            ganancia += 3*base13
    else:
        if 25 <= numero <= 36:
            ganancia+= 3*base13
    if apuestaRealizada[3] == 'filaInf':
        if numero % 3 == 1:
            ganancia += 3*base13
    elif apuestaRealizada[3] == 'filaMed':
        if numero % 3 == 2:
            ganancia += 3*base13
    else:
        if numero % 3 == 0:
            ganancia += 3*base13
    return ganancia
            
def otra_estrategia(tiradasPorCorrida, capitalArg): #Apostar 10 a las que tienen 1:2 y apostar 5 a las que tienen 1:3. Esta apuesta es fija
    capital = 0 if capitalArg == 'i' else 1000
    apuesta12 = 10 #Riesgo que tomo apostando 1:2
    apuesta13 = 5 #Riesgo que tomo apostando 1:3
    apuestaARealizar = (2*apuesta12 + 2*apuesta13)
    quebro = False
    historial = []
    historial_numeros = []
    ganancias = []
    retornos = ["r", "par", "inf", "filaInf"]
    for i in range(tiradasPorCorrida):
        numeroActual = tirada()
        historial_numeros.append(numeroActual)
        ganancia = evaluarTirada(numeroActual, retornos, apuesta12, apuesta13)
        capital += ganancia
        if capital > (apuestaARealizar) or capitalArg == 'i':
            historial.append(capital)
            ganancias.append(ganancia - apuestaARealizar)
            retornos = estrategia_optima(historial_numeros)
            capital -= apuestaARealizar
        else:
            quebro = True
            break
        
    return historial, quebro

## ------------------------ PROGRAMA PRINCIPAL

def main():
    args = parse_args()
    numeroDeCorridas = args.c
    tiradasPorCorrida = args.n
    estrategia = args.s
    capital  = args.a
    validar_argumentos(args)
    
    quiebras = 0
    historial_corridas = []

    for corrida in range(numeroDeCorridas):
        if estrategia == 'm':
            resultado, quebro = martingala(tiradasPorCorrida, capital) 
        elif estrategia == 'd':
            resultado, quebro = dalembert(tiradasPorCorrida, capital) 
        elif estrategia == 'f':
            resultado, quebro = fibonacci(tiradasPorCorrida, capital)
        elif estrategia == 'o':
            resultado, quebro = otra_estrategia(tiradasPorCorrida, capital) 
        
        if quebro is True : 
            quiebras += 1

        historial_corridas.append(resultado)

    graficar(historial_corridas, quiebras, estrategia, capital, tiradasPorCorrida)


if __name__ == '__main__': main()
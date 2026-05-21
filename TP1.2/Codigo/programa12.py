import random
import statistics
import matplotlib.pyplot as plt
import argparse
import sys

opcionesS = ['m', 'd', 'f', 'o']
opcionesA = ['i', 'f']
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

args = parse_args()
numeroDeCorridas = args.c
tiradasPorCorrida = args.n
estrategia = args.s
capital  = args.a

fib = [0] * 100
fib[0] = 1
fib[1] = 1
for i in range(2,51):
    fib[i] = fib[i-1] - fib[i-2]

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
for i in range(2,51):
    fib[i] = fib[i-1] - fib[i-2]

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

def dalembert(tiradas, capital):
    apuesta_base = 10
    apuesta_actual = apuesta_base
    capital_actual = capital
    historial_tiradas = []

    for i in range(tiradas):
        # 1. Girar la ruleta
        numero = random.randint(0, 36)
        gano = numero != 0 and numero % 2 == 0  # apuesta a números pares

        # 2. Actualizar capital si es finito
        if capital_actual is not None:
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
        if capital_actual is not None and capital_actual <= 0:
            break

    return historial_tiradas

idx = 0
def fibonacci():
    gamble = 'r'
    capital = 1000
    idx = 0
    apuesta = fib[idx] * 5
    historial = [capital]
    for _ in range(tiradasPorCorrida):
        if gamble == 'r':
            if tirada() in red:
                capital += apuesta
                apuesta = 5
                idx = 0
            else:
                capital -= apuesta
                idx += 1
                apuesta = min(capital, 5*fib[idx])
                if apuesta == 0:
                    print(f"Quebró en la corrida {_+1}")
                    break
        else:
            if tirada() not in red:
                capital += apuesta
                apuesta = 5
                idx = 0
            else:
                capital -= apuesta
                idx += 1
                apuesta = min(capital, 5*fib[idx])
                if apuesta == 0:
                    print(f"Quebró en la corrida {_+1}")
                    break

def main():
    args = parse_args()
    validar_argumentos(args)
    capital = None if args.a == 'i' else 1000
    quiebras = 0
    historial_corridas = []

    for corrida in range(args.c):
        if args.s == 'm':
            resultado, quebro = martingala(args.n, capital)
        elif args.s == 'd':
            resultado, quebro = dalembert(args.n, capital)
        elif args.s == 'f':
            resultado, quebro = fibonacci(args.n, capital)
        elif args.s == 'o':
            resultado, quebro = otra_estrategia(args.n, capital)
        
        if quebro : 
            quiebras += 1

        historial_corridas.append(resultado)

def martingala(tiradas, capital):

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

    return {
        "historial": historial_capital,
        "capital_final": capital_actual,
        "quebrado": quebrado
    }
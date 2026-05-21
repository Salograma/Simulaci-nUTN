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


idx = 0
def fibonacci():
    gamble = 'r'
    for i in range(numeroDeCorridas):
        capital = 1000
        idx = 0
        apuesta = fib[idx] * 5
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
                        print(f"Quebró en la corrida {i+1}")
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
                        print(f"Quebró en la corrida {i+1}")
                        break

match estrategia:
    case 'f':
        fibonacci()

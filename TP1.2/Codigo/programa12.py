import random
import statistics
import matplotlib.pyplot as plt
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Simulador de ruleta')
    parser.add_argument('-c', type=int, default=1,   help='Cantidad de corridas')
    parser.add_argument('-n', type=int, default=100, help='Tiradas por corrida')
    ###parser.add_argument('-e', type=int, default=7,   help='Número elegido (0-36)')
    parser.add_argument('-s', type=str, required=True, choices=['m', 'd', 'f', 'o'],
                        help='Estrategia: m=Martingala, d=DAlembert, f=Fibonacci, o=Otra')
    parser.add_argument('-a', type=str, required=True, choices=['i', 'f'],
                        help='Tipo de capital: i=infinito, f=finito')
    return parser.parse_args()


def validar_argumentos(args):
    errores = []

    if args.c <= 0:
        errores.append(f"Las corridas (-c) deben ser mayor a 0. Recibido: {args.c}")

    if args.n <= 0:
        errores.append(f"Las tiradas (-n) deben ser mayor a 0. Recibido: {args.n}")

    ###if numero_elegido < 0 or numero_elegido > 36:
        ###errores.append(f"Número inválido, debe ser entre 0 y 36.")

    if errores:
        for e in errores:
            print(f"[ERROR] {e}")
        sys.exit(1)


# Reemplazá los 3 input() por esto:
args = parse_args()
numeroDeCorridas = args.c
tiradasPorCorrida = args.n
###numero_elegido = args.e
estrategia = args.s
capital  =args.a



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



import random
import statistics
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Simulador de ruleta')
    parser.add_argument('-c', type=int, default=1,   help='Cantidad de corridas')
    parser.add_argument('-n', type=int, default=100, help='Tiradas por corrida')
    parser.add_argument('-e', type=int, default=7,   help='Número elegido (0-36)')
    return parser.parse_args()

# Reemplazá los 3 input() por esto:
args = parse_args()
numeroDeCorridas = args.c
tiradasPorCorrida = args.n
numero_elegido = args.e

if numero_elegido < 0 or numero_elegido > 36:
    print("Número inválido, debe ser entre 0 y 36.")
    exit()

print("Simulador de ruleta")

red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

def tirada():
    return random.randint(0, 36)

def frecuenciaRelativa(xi, n):
    return round(xi / n, 2)

"""print("Ingrese el número de corridas:")
numeroDeCorridas = int(input())

print("Ingrese el número de tiradas por corrida:")
tiradasPorCorrida = int(input())

print("Ingrese el número a elegir (0-36):")
numero_elegido = int(input())
if numero_elegido < 0 or numero_elegido > 36:
    print("Número inválido, debe ser entre 0 y 36.")
    exit()"""


# Valores esperados
fre = 1 / 37                                       # 0.027 (frecuencia relativa esperada)
vpe = sum(range(37)) / 37                         # 18.0 (valor promedio esperado)
vve = sum((x - vpe)**2 for x in range(37)) / 37  # ≈  114.5 (valor de la varianza de esperada)
vde = vve ** 0.5                                  # ≈ 10.7(valor del desvio esperado)

n = list(range(1, tiradasPorCorrida + 1))
corrida = 1

while corrida <= numeroDeCorridas:
    print(f"\n--- Corrida {corrida} ---")

    # Reiniciar acumulados
    frn = []
    vpn = []
    vdn = []
    vvn = []
    aciertos = 0
    suma_acumulada = 0
    valores_hasta_n = []
    redTh, blackTh, par = 0, 0, 0

    # Generar tiradas
    resultados = [tirada() for _ in range(tiradasPorCorrida)]

    for j, resultado in enumerate(resultados, start=1):
        if resultado in red:
            redTh += 1
        elif resultado != 0:
            blackTh += 1
        if resultado > 0 and resultado % 2 == 0:
            par += 1

        valores_hasta_n.append(resultado)
        suma_acumulada += resultado

        if resultado == numero_elegido:
            aciertos += 1

        frn.append(aciertos / j)
        vpn.append(suma_acumulada / j)

        if j >= 2:
            vdn.append(statistics.stdev(valores_hasta_n))
            vvn.append(statistics.variance(valores_hasta_n))
        else:
            vdn.append(0)
            vvn.append(0)

    greenTh = tiradasPorCorrida - (redTh + blackTh)
    impar = tiradasPorCorrida - par - greenTh

print("Frecuencia absoluta de rojas:", redTh)
print("Frecuencia absoluta de negras:", blackTh)
print("Frecuencia absoluta de verdes:", greenTh)
print("Frecuencia absoluta de pares:", par)
print("Frecuencia absoluta de impares:", impar)
print("Frecuencia relativa de rojas:", frecuenciaRelativa(redTh, tiradasPorCorrida))
print("Frecuencia relativa de negras:", frecuenciaRelativa(blackTh, tiradasPorCorrida))
print("Frecuencia relativa de verdes:", frecuenciaRelativa(greenTh, tiradasPorCorrida))
print("Frecuencia relativa de pares:", frecuenciaRelativa(par, tiradasPorCorrida))
print("Frecuencia relativa de impares:", frecuenciaRelativa(impar, tiradasPorCorrida))

modas = statistics.multimode(resultados)
print(
    f"{'Número' if len(modas) == 1 else 'Números'} más "
    f"{'frecuente' if len(modas) == 1 else 'frecuentes'}:",
    *(sorted(modas))
    )

# Gráfica - Frecuencia Relativa
plt.figure()
plt.title(f"Frecuencia Relativa - Corrida {corrida}")
plt.plot(n, frn, color="red", label="frn = frecuencia relativa")
plt.axhline(y=fre, color="blue", linewidth=2, label="fre = frecuencia relativa esperada")
plt.xlabel("n (número de tiradas)")
plt.ylabel("frecuencia relativa")
plt.legend()
plt.show()

# Gráfica - Valor promedio
plt.figure()
plt.title(f"Valor promedio - Corrida {corrida}")
plt.plot(n, vpn, color="red", label="vpn = valor promedio")
plt.axhline(y=vpe, color="blue", linewidth=2, label="vpe = valor promedio esperado")
plt.xlabel("n (número de tiradas)")
plt.ylabel("Valor promedio de las tiradas")
plt.legend()
plt.show()

# Gráfica - Valor del desvio
plt.figure()
plt.title(f"Valor del desvio - Corrida {corrida}")
plt.plot(n, vdn, color="red", label="vdn = valor del desvio")
plt.axhline(y=vde, color="blue", linewidth=2, label="vde = valor del desvio esperado")
plt.xlabel("n (número de tiradas)")
plt.ylabel("valor del desvio")
plt.legend()
plt.show()

# Gráfica - Valor de la varianza
plt.figure()
plt.title(f"Valor de la varianza - Corrida {corrida}")
plt.plot(n, vvn, color="red", label="vvn = valor de la varianza")
plt.axhline(y=vve, color="blue", linewidth=2, label="vve = valor de la varianza esperada")
plt.xlabel("n (número de tiradas)")
plt.ylabel("valor de la varianza")
plt.legend()
plt.show()

corrida += 1
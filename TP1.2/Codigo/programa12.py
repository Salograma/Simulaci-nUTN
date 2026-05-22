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

def reinicio(capital, apuesta, idx):
    capital += apuesta
    apuesta = 5
    idx = 0
    return capital, apuesta, idx

idx = 0
def fibonacci():
    if estrategia == 'f':
        gamble = 'r'
        idx = 0
        apuesta = fib[idx] * 5
        historial = [capital]
        estaQuebrado = False
        for _ in range(tiradasPorCorrida):
            if gamble == 'r':
                if tirada() in red:
                    capital, apuesta, idx = reinicio(capital, apuesta, idx)
                else:
                    capital -= apuesta
                    idx += 1
                    apuesta = min(capital, 5*fib[idx])
                    if apuesta == 0:
                        print(f"Quebró en la tirada {_+1}")
                        historial.append(capital)
                        break
                historial.append(capital)
            else:
                if tirada() not in red:
                    capital, apuesta, idx = reinicio(capital, apuesta, idx)
                else:
                    capital -= apuesta
                    idx += 1
                    apuesta = min(capital, 5*fib[idx])
                    if apuesta == 0:
                        print(f"Quebró en la tirada {_+1}")
                        historial.append(capital)
                        break
                historial.append(capital)
        if capital == 0:
            estaQuebrado = True
    else:
        gamble = 'b'
        idx = 0
        apuesta = fib[idx] * 5
        historial = [capital]
        estaQuebrado = None
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
            else:
                if tirada() not in red:
                    capital += apuesta
                    apuesta = 5
                    idx = 0
                else:
                    capital -= apuesta
                    idx += 1
                    apuesta = min(capital, 5*fib[idx])
    return historial, estaQuebrado

def estrategia_optima(ultimasJugadas):
    retornos = ["r", "par", "inf", "filaInf"]
    jugada = ultimasJugadas[0]
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
            
def otra_estrategia(tiradasPorCorrida, capital): #Apostar 10 a las que tienen 1:2 y apostar 5 a las que tienen 1:3. Esta apuesta es fija
    apuesta12 = 10 #Riesgo que tomo apostando 1:2
    apuesta13 = 5 #Riesgo que tomo apostando 1:3
    apuestaARealizar = (2*apuesta12 + 2*apuesta13)
    quebro = False
    historial = []
    ganancias = []
    retornos = ["r", "par", "inf", "filaInf"]
    for i in range(tiradasPorCorrida):
        capital -= apuestaARealizar
        numeroActual = tirada()
        historial.append(numeroActual)
        ganancia = evaluarTirada(numeroActual, retornos, apuesta12, apuesta13)
        capital += ganancia
        if capital > (apuestaARealizar):
            ganancias.append(ganancia - apuestaARealizar)
            retornos = estrategia_optima(historial)
            capital -= apuestaARealizar
        else:
            quebro = True
            break
    return historial, quebro
    
def main():
    args = parse_args()
    validar_argumentos(args)
    capital = 0 if args.a == 'i' else 1000
    quiebras = 0
    historial_corridas = []

    for corrida in range(args.c):
        if args.s == 'm':
            resultado, quebro = martingala(args.n, capital) #no reciben parametros de entrada
        elif args.s == 'd':
            resultado, quebro = dalembert(args.n, capital) #no reciben parametros de entrada
        elif args.s == 'f':
            resultado, quebro = fibonacci()
        elif args.s == 'o':
            resultado, quebro = otra_estrategia(args.n, capital) #no reciben parametros de entrada
        
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
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
    capital = None if capitalArg == 'i' else 1000
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
    capital_actual = 0 if capitalArg == 'i' else 1000
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
        capital = 1000
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


if __name__ == '__main__': main()
import random
import time
import numpy

def validarRestriccionesB(matrizB, M_max, C, M):
    # CADA MÁQUINA PUEDE PERTENECER A UNA SOLA CELDA
    for i in range(M):
        if sum(matrizB[i]) != 1:
            return False
    # EL M_max DE MAQUINAS QUE PUEDE CONTENER UNA CELDA
    for k in range(C):
        if sum(matrizB[i][k] for i in range(M)) > M_max:
            return False
    return True

def validarMatrizC(matrizC, P):
    # CADA PIEZA PUEDE PERTENECER A UNA SOLA CELDA
    for c in range(P):
        if sum(matrizC[c]) != 1:
            return False
    return True

def crea_matrizB(C, M_max, matriz, M, P):
    matrizB = [[0 for _ in range(C)] for _ in range(M)]
    for i in range(M):
        celda = random.randint(0, C - 1)
        matrizB[i][celda] = 1
    return matrizB

        
def crea_matrizC(matrizB, P, C):
    # GENERAR MATRIZ ALEATORIA C (ASIGNACIÓN DE PIEZAS A CELDAS)
    matrizC = [[0 for _ in range(C)] for _ in range(P)]
    for i in range(P):
        # Asignar a cada pieza i una celda aleatoria
        celda = random.randint(0, C - 1)
        matrizC[i][celda] = 1
    return matrizC

# FUNCIÓN OBJETIVO PARA EVALUAR UNA SOLUCIÓN (MINIMIZAR EL COSTO)
def funcionObjetivo(M, C, P, matrizA, matrizB, matrizC):
    score = 0
    for k in range(C):
        for i in range(M):
            for j in range(P):
                score += matrizA[i][j] * matrizC[j][k] * (1 - matrizB[i][k])
    return score

# CREAR UN MAPA QUE CUENTE LA CANTIDAD DE MÁQUINAS ASIGNADAS A CADA CELDA
def crearMapa(matriz, columna, fila):
    mapa = {}
    for celda in range(columna):
        sumaMaquinas = 0
        for maquina in range(fila):
            sumaMaquinas += matriz[maquina][celda]
        mapa[celda] = sumaMaquinas
    return mapa

# REPARAR MATRIZ B PARA CUMPLIR LAS RESTRICCIONES TOMANDO SOLUCION NO VIABLE EN VIABLE
def repararMatrizB(matrizB, M, C, M_max):
    # ARREGLA LA PRIMERA RESTRICCIÓN (CADA MÁQUINA PERTENECE A UNA SOLA CELDA)
    for maquina in range(M):
        for celda in range(C):
            if sum(matrizB[maquina]) > 1:
                while sum(matrizB[maquina]) > 1:
                    matrizB[maquina][celda] = 0
            elif sum(matrizB[maquina]) < 1:
                while sum(matrizB[maquina]) < 1:
                    matrizB[maquina][celda] = 1

    # CREAR UN MAPA PARA CUMPLIR LA SEGUNDA RESTRICCIÓN (MÁXIMO MÁQUINAS POR CELDA)
    mapaCeldasMaquinas = crearMapa(matrizB, C, M)

    # REPARAR LA MATRIZ PARA CUMPLIR LA SEGUNDA RESTRICCIÓN
    for maquina in range(M):
        for celda in range(C):
            if mapaCeldasMaquinas[celda] > M_max:
                if matrizB[maquina][celda] == 1:
                    matrizB[maquina][celda] = 0
                    matrizB[maquina][0 if celda == C - 1 else celda + 1] = 1
                mapaCeldasMaquinas = crearMapa(matrizB, C, M)
    return matrizB


def repararMatrizC(matrizC,P,C):
    for pieza in range(P):
        for celda in range(C):
            if sum(matrizC[pieza]) > 1:
                while sum(matrizC[pieza]) > 1:
                    matrizC[pieza][celda] = 0
            elif sum(matrizC[pieza]) < 1:
                while sum(matrizC[pieza]) < 1:
                    matrizC[pieza][celda] = 1
    return matrizC

def imprimirMatrizB(matrizB):
    # IMPRIMIR LA MATRIZ B
    print("\nMejor matriz B MAQUINA-CELDA")
    print("   C1-C2")
    i = 1
    for maquina in matrizB:
        print(f"M{i}{maquina}")
        i += 1

# FUNCIÓN PARA GENERAR UN VECINO (MODIFICAR ALEATORIAMENTE UNA MÁQUINA O PIEZA DE CELDA)
def generar_vecino(matrizB, matrizC, M, C, P):
    # HACER UNA COPIA DE LAS MATRICES PARA MODIFICAR
    nueva_matrizB = [fila[:] for fila in matrizB]
    nueva_matrizC = [fila[:] for fila in matrizC]

    # MODIFICAR ALEATORIAMENTE UNA CELDA DE LA MATRIZ B (MÁQUINA-CELDA)
    maquinaRand = random.randint(0, M - 1)
    
    # ENCONTRAR CELDA ACTUAL DE LA MÁQUINA, VALIDAR QUE HAYA UN 1
    if 1 in nueva_matrizB[maquinaRand]:
        celda_actual = nueva_matrizB[maquinaRand].index(1)  # Obtener la celda actual de la máquina
    else:
        # Si no hay ninguna celda asignada, asignar una nueva aleatoriamente
        celda_actual = random.randint(0, C - 1)
        nueva_matrizB[maquinaRand][celda_actual] = 1
    
    nueva_matrizB[maquinaRand][celda_actual] = 0  # DESASIGNAR DE LA CELDA ACTUAL
    
    # EVITAR QUE SE QUEDE SIN CELDA ASIGNADA
    nueva_celda = random.choice([k for k in range(C) if k != celda_actual])  # Asignar una nueva celda diferente
    nueva_matrizB[maquinaRand][nueva_celda] = 1  # Asignar a una nueva celda aleatoria

    # MODIFICAR ALEATORIAMENTE UNA CELDA DE LA MATRIZ C (PIEZA-CELDA)
    pieza = random.randint(0, P - 1)
    celda_actual = nueva_matrizC[pieza].index(1)
    nueva_matrizC[pieza][celda_actual] = 0
    nueva_celda = random.choice([k for k in range(C) if k != celda_actual])
    nueva_matrizC[pieza][nueva_celda] = 1

    return nueva_matrizB, nueva_matrizC




# FUNCION DE RECALCULO DE TEMPERATURA EN EL SIMULATED ANNEALING
def calcular_temperatura(temperatura, factor_enfriamiento):
    return temperatura * factor_enfriamiento

# IMPLEMENTACIÓN DEL SIMULATED ANNEALING
def simulated_annealing(matrizA, M, P, C, M_max, temperatura_inicial, factor_enfriamiento, iteraciones):
    # INICIALIZAR LA MEJOR SOLUCIÓN CON UNA SOLUCIÓN ALEATORIA
    mejor_matrizB = crea_matrizB(C, M_max, matrizA, M, P)
    mejor_matrizC = crea_matrizC(mejor_matrizB, P, C)
    mejor_score = funcionObjetivo(M, C, P, matrizA, mejor_matrizB, mejor_matrizC)

    mejor_matrizB = repararMatrizB(mejor_matrizB,M,C,M_max)
    mejor_matrizC = repararMatrizC(mejor_matrizC,P,M)
    # INICIALIZAR LA TEMPERATURA
    temperatura = temperatura_inicial

    for _ in range(iteraciones):
        # GENERAR UNA NUEVA SOLUCIÓN VECINA
        nueva_matrizB, nueva_matrizC = generar_vecino(mejor_matrizB, mejor_matrizC, M, C, P)
        nueva_matrizB = repararMatrizB(nueva_matrizB,M,C,M_max)
        nueva_matrizC = repararMatrizC(nueva_matrizC,P,C)
        nuevo_score = funcionObjetivo(M, C, P, matrizA, nueva_matrizB, nueva_matrizC)

        # SI LA NUEVA SOLUCIÓN ES MEJOR, LA ACEPTAMOS
        if nuevo_score < mejor_score:
            mejor_matrizB, mejor_matrizC = nueva_matrizB, nueva_matrizC
            mejor_score = nuevo_score
        else:
            # ACEPTAR SOLUCIÓN PEOR CON CRITERIO DE ACEPTACION
            delta = nuevo_score - mejor_score
            probabilidad_aceptacion = numpy.exp(-delta / (temperatura + 1e-10))##numpy.exp(-delta / temperatura)
            if random.random() < probabilidad_aceptacion:
                mejor_matrizB, mejor_matrizC = nueva_matrizB, nueva_matrizC
                mejor_score = nuevo_score

        # REDUCIR LA TEMPERATURA
        temperatura = calcular_temperatura(temperatura, factor_enfriamiento)

    return mejor_matrizB, mejor_matrizC, mejor_score

# APLICACIÓN DE LA OPTIMIZACIÓN MCDP USANDO SIMULATED ANNEALING
def mcdp(C, M_max, matrizA, M, P):
    exTime = time.time()  # TIEMPO INICIO

    # PARÁMETROS DEL SIMULATED ANNEALING
    temperatura_inicial = 10000
    factor_enfriamiento = 0.5
    iteraciones = 10

    # EJECUTAR SIMULATED ANNEALING PARA OPTIMIZACIÓN
    mejor_matrizB, mejor_matrizC, mejor_score =  simulated_annealing(matrizA, M, P, C, M_max, temperatura_inicial, factor_enfriamiento, iteraciones)

    # MOSTRAR RESULTADOS OPTIMIZADOS
    print("\nSimulated Annealing")
    imprimirMatrizB(mejor_matrizB)  # MEJOR MATRIZ B (MAQUINAS-CELDAS)
    print("\n")
    
    print("\nMejor matriz C PIEZA-CELDA")
    for i, pieza in enumerate(mejor_matrizC, start=1):
        print(f"P{i}: {pieza}")
    
    # MEJOR SCORE ALCANZADO
    print(f"\nMejor Score (costo): {mejor_score}")
    print(f"Tiempo de ejecución: {round(time.time() - exTime, 2)} segundos")
    return

matrizA = [
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
]

# LLAMADA A LA FUNCIÓN MCDP
num_maquina = len(matrizA)
num_piezas = len(matrizA[0])

mcdp(2, 8, matrizA, num_maquina, num_piezas)
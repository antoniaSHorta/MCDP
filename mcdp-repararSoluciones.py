import random
import time
import numpy

def validarRestriccionesB(matrizB, M_max, C, M):
    # CADA MAQUINA PUEDE PERTENECER A UNA CELDA
    for i in range(M):
        if sum(matrizB[i]) != 1:
            return False
    # EL M_max DE MAQUINAS QUE PUEDE CONTENER UNA CELDA
    for k in range(C):
        if sum(matrizB[i][k] for i in range(M)) > M_max:
            return False
    return True

def validarMatrizC(matrizC, P):
    for c in range(P):
        if sum(matrizC[c]) != 1:
            return False
    return True

def crea_matrizB(c, m_max, matriz, m, p):
    matrizB = []
    for _ in range(m):
        fila = []
        for _ in range(c):
            fila.append(random.randint(0, 1))
        matrizB.append(fila)
    return matrizB
        
def crea_matrizC(matrizB, P, C):
    while True:
        matrizC = []
        for i in range(P):
            fila = [random.randint(0, 1) for _ in range(C)]
            matrizC.append(fila)
        return matrizC

def funcionObjetivo(M,C,P, matrizA, matrizB, matrizC):
    score = 0
    for k in range(C):
        for i in range(M):
            for j in range(P):
                score += matrizA[i][j]*matrizC[j][k]*(1-matrizB[i][k])
    return score

def crearMapa(matriz,columna,fila):
    mapa={}
    for celda in range(columna):
        sumaMaquinas = 0
        for maquina in range(fila):
            sumaMaquinas+=matriz[maquina][celda]
        mapa[celda]=sumaMaquinas
    return mapa

# Se toma una solución no viable y se convierte en una viable
def repararMatrizB(matrizB,M,C,M_max):
    imprimirMatrizB(matrizB)
    # Arreglamos la matriz para que cumpla la primera restricción
    for maquina in range(M):
        for celda in range (C):
            if(sum(matrizB[maquina])>1):
                while(sum(matrizB[maquina]) > 1):
                    matrizB[maquina][celda] = 0
            elif(sum(matrizB[maquina]) < 1):
                while(sum(matrizB[maquina]) < 1):
                    matrizB[maquina][celda] = 1 

    # Contamos las máquinas que hay asignadas a cada celda y las ponemos en un para comprobar la restricción 2
    mapaCeldasMaquinas = crearMapa(matrizB,C,M)    

    # Arreglamos la matriz para que cumpla la segunda restricción
    for maquina in range(M):
        for celda in range (C):
            if(mapaCeldasMaquinas[celda]>M_max):
                if(matrizB[maquina][celda]==1):
                    matrizB[maquina][celda] = 0
                    matrizB[maquina][0 if celda == C - 1 else celda + 1] = 1
                mapaCeldasMaquinas=crearMapa(matrizB,C,M) 

    return matrizB

def imprimirMatrizB(matrizB):
    print("\nMejor matriz B MAQUINA-CELDA")
    print("   C1-C2")
    i = 1
    for maquina in matrizB:
        print(f"M{i}{maquina}")
        i+=1

def mcdp(C, M_max, matrizA, M, P):
    exTime = time.time()
    epochs = 100
    bestMatrizB = []
    bestMatrizC = []
    bestScore = 0

    matrizB = crea_matrizB(C, M_max, matrizA, M, P)
    imprimirMatrizB(matrizB)
    matrizC = crea_matrizC(matrizB, P, C)
    # matrizB=[[0,0],
    #          [0,0],
    #          [0,0],
    #          [0,0],
    #          [0,0]]

    matrizB = repararMatrizB(matrizB,M,C,M_max)
    
    # print(f"Número de ciclos = {epochs}")

    # print("\nMatriz A MAQUINA-PIEZA")
    # print("   P1-P2-P3-P4-P5-P6-P7")
    # i = 1
    # for maquina in matrizA:
    #     print(f"M{i}{maquina}")
    #     i+=1

    imprimirMatrizB(matrizB)

    # print("\nMejor matriz C PIEZA-CELDA")
    # print("   C1-C2")
    # i = 1
    # for pieza in matrizC:
    #     print(f"P{i}{pieza}")
    #     i+=1
    
    # print(f"Movimiento entre celdas = {bestScore}")
    # print(f"Tiempo de ejecución = {round(time.time() - exTime,2)} segundos")

    return

# MAIN
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

# LLAMADA A FUNCIONES
num_maquina = len(matrizA)
num_piezas = len(matrizA[0])
mcdp(2, 8, matrizA, num_maquina, num_piezas)
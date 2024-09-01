import random

def validarRestricciones(matrizB, M_max, C, P, M):
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

def optimizar():
    return

def mcdp(C, M_max, matrizA, M, P):
    epochs = 100
    bestMatrizB = []
    bestMatrizC = []
    bestScore = 0
    for epoch in range(epochs):
        matrizB = crea_matrizB(C, M_max, matrizA, M, P)

        while not validarRestricciones(matrizB, M_max, C, P, M):
            matrizB = crea_matrizB(C, M_max, matrizA, M, P)
        matrizC = crea_matrizC(matrizB, P, C)

        while not validarMatrizC(matrizC, P):
            matrizC = crea_matrizC(matrizB,P,C)
        
        score = funcionObjetivo(M,C,P,matrizA, matrizB, matrizC)
        if(bestScore == 0 or score < bestScore):
            bestScore = score
            bestMatrizB = matrizB
            bestMatrizC = matrizC
    
    print(f"Número de ciclos = {epochs}")

    print("Matriz A MAQUINA-PIEZA")
    print("   P1-P2-P3-P4-P5-P6-P7")
    i = 1
    for maquina in matrizA:
        print(f"M{i}{maquina}")
        i+=1

    print("\nMejor matriz B MAQUINA-CELDA")
    print("   C1-C2")
    i = 1
    for maquina in bestMatrizB:
        print(f"M{i}{maquina}")
        i+=1
    print("\nMejor matriz C PIEZA-CELDA")
    print("   C1-C2")
    i = 1
    for pieza in bestMatrizC:
        print(f"P{i}{pieza}")
        i+=1
    
    print(f"Movimiento entre celdas = {bestScore}")

    return

# MAIN
matrizA = [
    [1,1,1,0,0,0,0],
    [1,1,1,0,0,1,0],
    [0,0,1,1,0,1,1],
    [0,1,1,0,1,1,0],
    [1,1,0,1,1,0,0],
]

# LLAMADA A FUNCIONES
num_maquina = len(matrizA)
num_piezas = len(matrizA[0])
mcdp(2, 3, matrizA, num_maquina, num_piezas)
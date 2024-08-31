
import random
def validarRestricciones(matrizB, M_max,C,P,M):
    # CADA MAQUINA PUEDE PERTENECER A UNA CELDA
    for i in range(M):
        if sum(matrizB[i]) != 1:
            return False
    # EL M_max DE MAQUINAS QUE PUEDE CONTENER UNA CELDA
    for k in range(C):
        if sum(matrizB[i][k] for i in range(M)) > M_max:
            return False
    return True

def crea_matrizB(c,m_max, matriz, m, p):
    matrizB = []

    for i in range(m):
        fila =[]
        for j in range(c):
            fila.append(random.randint(0,1))
        matrizB.append(fila)
    return matrizB


def crea_matrizC(matrizB,P,C):
    while True:
        matrizC = []
        for i in range(P):
            fila = [random.randint(0,1) for _ in range(C)]
            matrizC.append(fila)
        if all(sum(fila) == 1 for fila in matrizC):
            return matrizC

def mcdp(C,M_max,matriz,M,P):
    matrizB = crea_matrizB(C,M_max,matriz,M,P)
    while not validarRestricciones(matrizB, M_max,C,P,M):
        matrizB = crea_matrizB(C,M_max,matriz,M,P)
    resultado = crea_matrizC(matrizB,P,C)
    print("")
    for fila in matrizB:
        print(fila)
    print("")
    for fila in resultado:
        print(fila)
    return resultado

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
mcdp(2,3,matrizA,num_maquina,num_piezas)

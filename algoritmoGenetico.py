import random
import time

# VALIDACION RESTRICCIONES MATRIZ B
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

# VALIDACION RESTRICCIONES MATRIZ C
def validarMatrizC(matrizC, P):
    # CADA PIEZA PUEDE PERTENECER A UNA SOLA CELDA
    for c in range(P):
        if sum(matrizC[c]) != 1:
            return False
    return True

# CREA UNA MATRIZ B DE MANERA ALEATORIA Y RETORNA UNA SOLUCION VIABLE AL REPARARLA
def crea_matrizB(C, M_max, M):
    matrizB = [[0 for _ in range(C)] for _ in range(M)]
    for i in range(M):
        celda = random.randint(0, C - 1)
        matrizB[i][celda] = 1
    return repararMatrizB(matrizB,M,C,M_max)

# CREA UNA MATRIZ c DE MANERA ALEATORIA Y RETORNA UNA SOLUCION VIABLE AL REPARARLA       
def crea_matrizC(P, C):
    matrizC = [[0 for _ in range(C)] for _ in range(P)]
    for i in range(P):
        celda = random.randint(0, C - 1)
        matrizC[i][celda] = 1
    return repararMatrizC(matrizC,P,C)

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

# REPARAR MATRIZ B PARA CUMPLIR LAS RESTRICCIONES TOMANDO SOLUCION NO VIABLES EN VIABLES
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

# REPARAR MATRIZ C PARA CUMPLIR LAS RESTRICCIONES TOMANDO SOLUCION NO VIABLES EN VIABLES
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

# IMPRIMIR LA MATRIZ B
def imprimirMatrizB(matrizB):
    print("\nMatriz B MAQUINA-CELDA")
    print("   " + " ".join(f"C{celda+1}" for celda in range(len(matrizB[0]))))
    for i,maquina in enumerate(matrizB, start=1):
        print(f"M{i} {maquina}")
    
# IMPRIMIR LA MATRIZ C    
def imprimirMatrizC(matrizC):
    print("\nMatriz C PIEZA-CELDA")
    print("   " + " ".join(f"C{celda+1}" for celda in range(len(matrizC[0]))))
    for i,pieza in enumerate(matrizC, start=1):
        print(f"P{i} {pieza}")

# GENERAR POBLACION INICIAL DE MANERA ALEATORIA
def crearPoblacionInicial(tam_poblacion,C,M_max,M,P,matrizA):
    poblacion=[]
    for _ in range(tam_poblacion):
        matriz_B = crea_matrizB(C, M_max, M)
        matriz_B 
        matriz_C = crea_matrizC(P, C)
        costo = funcionObjetivo(M, C, P, matrizA, matriz_B, matriz_C)
        poblacion.append((matriz_B, matriz_C, costo))
    return poblacion

# FUNCIÓN PARA LA SELECCIÓN POR RULETA
def seleccion_ruleta(poblacion):
    total_fitness = sum(1 / individuo[2] for individuo in poblacion)

    seleccion = random.uniform(0, total_fitness)
    
    # RECORRER
    acumulado = 0
    for individuo in poblacion:
        acumulado += 1 / individuo[2]
        if acumulado >= seleccion:
            return individuo
    
    return poblacion[-1]  # ERRORES DE REDONDEO

# FUNCIÓN DE CRUZAMIENTO UNIFORME
def cruzamiento_uniforme(padre1, padre2):

    #IMPLEMENTACION DE CRUZAMIENTO 
    hijo1_B = [[0 for _ in range(len(padre1[0][0]))] for _ in range(len(padre1[0]))]
    hijo2_B = [[0 for _ in range(len(padre1[0][0]))] for _ in range(len(padre1[0]))]
    hijo1_C = [[0 for _ in range(len(padre1[1][0]))] for _ in range(len(padre1[1]))]
    hijo2_C = [[0 for _ in range(len(padre1[1][0]))] for _ in range(len(padre1[1]))]
    
    # CRUZAMIENTO UNIFORME MATRIZ B
    for i in range(len(padre1[0])):
        for j in range(len(padre1[0][0])):
            if random.random() < 0.5:
                hijo1_B[i][j] = padre1[0][i][j]
                hijo2_B[i][j] = padre2[0][i][j]
            else:
                hijo1_B[i][j] = padre2[0][i][j]
                hijo2_B[i][j] = padre1[0][i][j]
    
    # CRUZAMIENTO UNIFORME MATRIZ C
    for i in range(len(padre1[1])):
        for j in range(len(padre1[1][0])):
            if random.random() < 0.5:
                hijo1_C[i][j] = padre1[1][i][j]
                hijo2_C[i][j] = padre2[1][i][j]
            else:
                hijo1_C[i][j] = padre2[1][i][j]
                hijo2_C[i][j] = padre1[1][i][j]
    
    return hijo1_B, hijo1_C, hijo2_B, hijo2_C

# FUNCIÓN DE MUTACIÓN
def mutacion_bit_flip(matriz, probabilidad):
    matriz_mutada = [fila[:] for fila in matriz]
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if random.random() < probabilidad:
                matriz_mutada[i][j] = 1 - matriz_mutada[i][j]
    if(validarRestriccionesB):
        return matriz_mutada
    else:
        return matriz


def genetico(matrizA, M, P, C, M_max, tam_poblacion, tasa_mutacion, num_generaciones):
    # DEFINE MEJOR SOLUCIÓN ENCONTRADA PARA COMPROBAR ESTANCAMIENTOS
    mejorCosto = 1000000000000
    cont = 0
    # GENERAR POBLACION ALEATORIA
    poblacion = crearPoblacionInicial(tam_poblacion,C,M_max,M,P,matrizA)
    
    # EVOLUCION
    for gen in range(num_generaciones):
        # GENERAR HIJOS (λ = tam_poblacion)
        hijos = []
        for _ in range(tam_poblacion):
            # SELECCION DE PADRES RULETA
            padre1 = seleccion_ruleta(poblacion)
            padre2 = seleccion_ruleta(poblacion)
            
            # CRUZAMIENTO UNIFORME
            hijo1_B, hijo1_C, hijo2_B, hijo2_C = cruzamiento_uniforme(padre1, padre2)
            
            # MUTACION BIT FLIP
            hijo1_B = mutacion_bit_flip(hijo1_B, tasa_mutacion)
            hijo1_C = mutacion_bit_flip(hijo1_C, tasa_mutacion)
            hijo2_B = mutacion_bit_flip(hijo2_B, tasa_mutacion)
            hijo2_C = mutacion_bit_flip(hijo2_C, tasa_mutacion)
            
            # RESPARAR SOLUCIONES
            hijo1_B = repararMatrizB(hijo1_B, M, C, M_max)
            hijo2_B = repararMatrizB(hijo2_B, M, C, M_max)
            hijo1_C = repararMatrizC(hijo1_C, P, C)
            hijo2_C = repararMatrizC(hijo2_C, P, C)
            
            # EVALUAMOS HIJOS
            costo1 = funcionObjetivo(M, C, P, matrizA, hijo1_B, hijo1_C)
            costo2 = funcionObjetivo(M, C, P, matrizA, hijo2_B, hijo2_C)
            
            hijos.extend([(hijo1_B, hijo1_C, costo1), (hijo2_B, hijo2_C, costo2)])
        
        # ESTRATEGIA  (μ + λ): UNIR PADRES E HIJOS
        poblacion_total = poblacion + hijos
        
        # SELECCION ELITISTA: SELECCIONAR LOS MEJORES tam_poblacion INDIVIDUOS
        poblacion_total.sort(key=lambda x: x[2])
        poblacion = poblacion_total[:tam_poblacion]
        
        # ITERACIONES
        mejor_actual = poblacion[0]
        
        # SE COMPRUEBA SI LA FUNCIÓN OBJETIVO NO MEJORA PARA DETENER EL PROGRAMA, YA QUE SIGNIFICA QUE PROBABLEMENTE ENCONTRÓ EL MÍNIMO FINAL (NO EL GLOBAL NECESARIAMENTE)
        if(mejorCosto == mejor_actual[2]):
            cont+=1
            if(cont==80):
                print("No se muestra mejora, deteniendo el programa...")
                return poblacion[0]
        else:
            mejorCosto = funcionObjetivo(M, C, P, matrizA, mejor_actual[0], mejor_actual[1])
            cont=0

        print(f"Generación {gen + 1}: Mejor costo = {mejor_actual[2]}")
    
    return poblacion[0]

# APLICACIÓN DE LA OPTIMIZACIÓN MCDP USANDO ALGORITMO GENETICO
def mcdp(C, M_max, matrizA, M, P):
    tiempo_inicio = time.time()  # TIEMPO INICIO

    # PARÁMETROS DEL ALGORITMO GENETICO
    tam_poblacion = 10
    tasa_mutacion = 0.1
    num_generaciones = 100

    # EJECUTAR ALGORITMO GENETICO PARA OPTIMIZACIÓN
    mejor_matrizB, mejor_matrizC, mejor_score =  genetico(matrizA, M, P, C, M_max, tam_poblacion, tasa_mutacion, num_generaciones)

    # MOSTRAR RESULTADOS OPTIMIZADOS
    print("\nAlgoritmo Genetico")
    imprimirMatrizB(mejor_matrizB)
    print()
    imprimirMatrizC(mejor_matrizC)
    
    tiempo_ejecucion=round(time.time() - tiempo_inicio, 2)

    # MEJOR SCORE ALCANZADO
    print(f"\nMejor costo encontrado: {mejor_score}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")

    return mejor_matrizB, mejor_matrizC, mejor_score, tiempo_ejecucion


# INSTANCIAS 

matrizA1 =[
    [1,1,1,0,1,0,0],
    [1,1,1,0,0,1,0],
    [0,0,1,1,0,1,1],
    [0,1,1,0,1,1,0],
    [1,1,0,1,1,0,0],
]

matrizA2 = [
    [0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,1,0],
    [0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
    [0,0,1,1,0,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1],
    [0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,0,0,1,0,0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0],
    [1,0,1,1,0,0,1,0,0,0,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,1,1,1,1,1,1],
]

matrizA3 = [
    [1,0,1,1,0,0,1,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0],
    [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,1,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1],
    [1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [1,1,1,1,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,0,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,1,0,0,1,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0],
]

# LLAMADA A LA FUNCIÓN MCDP
print()
print("¿Qué instancia desea utilizar?\n")

print("1.- Instancia 1")
print("2.- Instancia 2")
print("3.- Instancia 3\n")

opcion = input("Seleccione una opción (1, 2 o 3): ")

if opcion == "1":
    mcdp(2, 3, matrizA1, len(matrizA1) , len(matrizA1[0]))
elif opcion == "2":
    mcdp(2, 8, matrizA2, len(matrizA2) , len(matrizA2[0]))
elif opcion == "3":
    mcdp(2, 8, matrizA3, len(matrizA3) , len(matrizA3[0]))
else:
    print("Opción no válida. Por favor, seleccione 1, 2 o 3.")
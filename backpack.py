import random
from itertools import product

objetos = [
    {"nombre": "Cuaderno", "peso": 1.2, "valor": 15},
    {"nombre": "Lápiz", "peso": 0.1, "valor": 5},
    {"nombre": "Plumones", "peso": 2.0, "valor": 25},
    {"nombre": "Regla", "peso": 0.5, "valor": 8},
    {"nombre": "Escuadra", "peso": 1.8, "valor": 20},
    {"nombre": "Calculadora", "peso": 0.7, "valor": 35},
    {"nombre": "Compás", "peso": 0.6, "valor": 12},
    {"nombre": "Libro de texto", "peso": 3.5, "valor": 50},
    {"nombre": "Tablet", "peso": 1.3, "valor": 55},
    {"nombre": "USB", "peso": 0.2, "valor": 10},
    {"nombre": "Agenda", "peso": 0.8, "valor": 18},
    {"nombre": "Colores", "peso": 1.1, "valor": 22}
]

CAPACIDAD_MAXIMA = 6
TAMANO_POBLACION = 30
TASA_MUTACION = 0.05
GENERACIONES_LIMITE = 1000

def generar_individuo():
    return [random.randint(0, 1) for _ in range(len(objetos))]

def generar_poblacion():
    return [generar_individuo() for _ in range(TAMANO_POBLACION)]

def calcular_fitness(individuo):
    peso_total = 0.0
    valor_total = 0
    for i in range(len(individuo)):
        if individuo[i] == 1:
            peso_total += objetos[i]["peso"]
            valor_total += objetos[i]["valor"]
    if peso_total > CAPACIDAD_MAXIMA:
        return 0
    return valor_total

def seleccion_ruleta(poblacion, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(poblacion)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individuo, fit in zip(poblacion, fitnesses):
        current += fit
        if current > pick:
            return individuo

def crossover(padre1, padre2):
    punto = random.randint(1, len(padre1) - 1)
    return padre1[:punto] + padre2[punto:]

def mutar(individuo):
    for i in range(len(individuo)):
        if random.random() < TASA_MUTACION:
            individuo[i] = 1 - individuo[i]
    return individuo

def obtener_valor_maximo_posible():
    max_valor = 0
    for combinacion in product([0, 1], repeat=len(objetos)):
        peso = sum(obj["peso"] for i, obj in enumerate(objetos) if combinacion[i])
        valor = sum(obj["valor"] for i, obj in enumerate(objetos) if combinacion[i])
        if peso <= CAPACIDAD_MAXIMA:
            max_valor = max(max_valor, valor)
    return max_valor

def mostrar_contenido_mochila(individuo):
    print("\n Mochila óptima contiene:")
    peso_total = 0.0
    valor_total = 0
    for i in range(len(individuo)):
        if individuo[i] == 1:
            obj = objetos[i]
            print(f" - {obj['nombre']} (Peso: {obj['peso']}kg, Valor: {obj['valor']})")
            peso_total += obj["peso"]
            valor_total += obj["valor"]
    print(f"\n Peso total: {peso_total:.2f}kg / {CAPACIDAD_MAXIMA}kg")
    print(f" Valor total: {valor_total}")

def algoritmo_genetico():
    poblacion = generar_poblacion()
    mejor_valor_global = 0
    mejor_solucion_global = None
    valor_optimo = obtener_valor_maximo_posible()
    generaciones = 0

    while generaciones < GENERACIONES_LIMITE:
        generaciones += 1
        fitnesses = [calcular_fitness(ind) for ind in poblacion]
        mejor = max(poblacion, key=calcular_fitness)
        mejor_valor = calcular_fitness(mejor)

        print(f"\n Generación {generaciones}")
        print(f" Mejor individuo: {mejor} | Valor educativo: {mejor_valor}")

        if mejor_valor > mejor_valor_global:
            mejor_valor_global = mejor_valor
            mejor_solucion_global = mejor

        if mejor_valor_global == valor_optimo:
            print("\n ¡Solución óptima encontrada!")
            mostrar_contenido_mochila(mejor_solucion_global)
            break

        nueva_poblacion = []
        while len(nueva_poblacion) < TAMANO_POBLACION:
            padre1 = seleccion_ruleta(poblacion, fitnesses)
            padre2 = seleccion_ruleta(poblacion, fitnesses)
            hijo = crossover(padre1, padre2)
            hijo = mutar(hijo)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion
    else:
        print("\n Se alcanzó el límite de generaciones sin encontrar la solución óptima.")
        mostrar_contenido_mochila(mejor_solucion_global)

if __name__ == "__main__":
    algoritmo_genetico()

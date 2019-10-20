from g_algorithm import geneticAlgorithm
import random
import matplotlib.pyplot as plt

OBJ_SIZE = 5
POP_SIZE = 20
SELECT_SIZE = 5
MUTATION_RATE = 0.1
ITERATIONS = 300
iterCount = 0
BOXES = [(12, 4),
         (2, 2),
         (1, 2),
         (1, 1),
         (4, 10)]
MAX_BOX_TYPE = 4  # Cuantas cajas se pueden usar de un tipo


def geneFunc():
    # Retorna cuantas cajas utilizar de un tipo.
    return random.randint(0, MAX_BOX_TYPE)


def fitnessFunc(obj):
    # Funcion de fitness = peso_mochila + 1 / (1 + valor_total).
    weight, value = 0, 0
    for i in range(OBJ_SIZE):
        weight += obj[i] * BOXES[i][0]
        value += obj[i] * BOXES[i][1]
    if weight > 15:
        return 0
    return weight + 1 / (1 + value)


def endCond():
    # Condicion de termino para un número de iteraciones.
    global iterCount
    iterCount += 1
    if iterCount >= ITERATIONS:
        iterCount = 0
        return True
    return False


def printSol(obj):
    totalWeight = 0
    totalValue = 0
    for i in range(OBJ_SIZE):
        weigth = BOXES[i][0]
        value = BOXES[i][1]
        totalWeight += weigth * obj[i]
        totalValue += value * obj[i]
        print("Cajas de {} kg: {}\t Valor: {}".format(
            weigth, obj[i], value * obj[i]))
    print("Peso total: {} kg\t Valor total: {}".format(totalWeight, totalValue))


# =================== Mejora de fitness por generación ======================= #

# Sin elitism
random.seed(42)
fitnessRecords = ([], [], [])  # Peor fitness, fitness promedio, mejor fitness
pop, best, bestFit = geneticAlgorithm(POP_SIZE, SELECT_SIZE, OBJ_SIZE,
                                      fitnessFunc, geneFunc, MUTATION_RATE,
                                      endCond, fitnessRecords=fitnessRecords)

print("Solución sin elitism:")
printSol(best)
print("Fitness de la solución:", bestFit)

x = [i for i in range(1, ITERATIONS)]
_, fitnessPlot = plt.subplots()
for y in fitnessRecords:
    fitnessPlot.plot(x, y)
fitnessPlot.legend(['Peor', 'Promedio', 'Mejor'])
fitnessPlot.set(xlabel='Generación', ylabel='Fitness',
                title='Fitness por generación sin elitism')

# Con elitism:
random.seed(42)
# Peor fitness, fitness promedio, mejor fitness
fitnessRecordsElitism = ([], [], [])
pop, best, bestFit = geneticAlgorithm(POP_SIZE, SELECT_SIZE, OBJ_SIZE,
                                      fitnessFunc, geneFunc, MUTATION_RATE,
                                      endCond, elitism=True, fitnessRecords=fitnessRecordsElitism)

print("\nSolución con elitism:")
printSol(best)
print("Fitness de la solución:", bestFit)

_, fitnessPlotElitism = plt.subplots()
for y in fitnessRecordsElitism:
    fitnessPlotElitism.plot(x, y)
fitnessPlotElitism.legend(['Peor', 'Promedio', 'Mejor'])
fitnessPlotElitism.set(xlabel='Generación', ylabel='Fitness',
                       title='Fitness por generación con elitsm')


# ========================= Heatmap configuraciones ========================== #

population = [i for i in range(50, 1001, 50)]
mutation_rate = [i/10 for i in range(11)]
heatmap = []
ITERATIONS = 100
iterCount = 0

for mut in mutation_rate:
    row = []
    for pop in population:
        select_size = int(pop / 10)
        _, _, bestFit = geneticAlgorithm(pop, select_size, OBJ_SIZE,
                                         fitnessFunc, geneFunc, mut, endCond, elitism=True)
        row.append(bestFit)
    heatmap.append(row)

fig, configsPlot = plt.subplots()
im = configsPlot.imshow(heatmap)

configsPlot.set_xticks([i for i in range(len(population))])
configsPlot.set_yticks([i for i in range(len(mutation_rate))])
configsPlot.set_yticklabels(mutation_rate)
configsPlot.set_xticklabels(population)
configsPlot.set(xlabel='Población', ylabel='Mutation rate',
                title="Heatmap fitness de las configuraciones")
fig.tight_layout()
plt.show()

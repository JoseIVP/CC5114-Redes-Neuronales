import random


def generateObject(objSize, geneFunc):
    return [geneFunc() for _ in range(objSize)]


def crossover(selection):
    obj1 = selection[random.randint(0, len(selection) - 1)]
    obj2 = selection[random.randint(0, len(selection) - 1)]
    objSize = len(obj1)
    cut = random.randint(0, objSize - 1)
    return obj1[0:cut] + obj2[cut:objSize], obj2[0:cut] + obj1[cut:objSize]


def mutate(obj, mutationRate, geneFunc):
    for i in range(len(obj)):
        if random.random() <= mutationRate:
            obj[i] = geneFunc()


def geneticAlgorithm(popSize, selectSize, objSize, fitnessFunc, geneFunc, mutationRate, endCond, elitism=False):
    population = [generateObject(objSize, geneFunc) for _ in range(popSize)]
    while not endCond():
        fitness = []
        bestObj, bestFitness = None, 0
        for obj in population:
            fitness.append(fitnessFunc(obj))
            if fitness[-1] >= bestFitness:
                bestObj = obj
                bestFitness = fitness[-1]

        # Roulette selection:
        fitnessAcc = [(fitness[i] + (0 if i == 0 else fitness[i-1]))
                      for i in range(popSize)]
        selection = []
        rands = [random.randint(0, fitnessAcc[-1]) for _ in range(selectSize)]
        rands.sort()
        j = 0
        for r in rands:
            while fitnessAcc[j] < r:
                j += 1
            selection.append(population[j])

        # Crossover:
        population = []
        for _ in range(int(popSize/2)):
            obj1, obj2 = crossover(selection)
            population.append(obj1)
            population.append(obj2)

        if popSize % 2 != 0:
            obj1, _ = crossover(selection)
            population.append(obj1)

        # Mutation:
        for obj in population:
            mutate(obj, mutationRate, geneFunc)

        if elitism:
            population[0] = bestObj

    return population, bestObj, bestFitness

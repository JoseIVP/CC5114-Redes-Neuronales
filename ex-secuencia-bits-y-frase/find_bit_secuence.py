from g_algorithm import geneticAlgorithm
import random

TARGET_SECUENCE = [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
OBJ_SIZE = 14
POP_SIZE = 10
SELECT_SIZE = 4
MUTATION_RATE = 0.1
ITERATIONS = 10
iterCount = 0


def geneFunc():
    return 0 if random.random() < 0.5 else 1


def fitnessFunc(obj):
    fitness = 0
    for i in range(OBJ_SIZE):
        if TARGET_SECUENCE[i] == obj[i]:
            fitness += 1
    return fitness


def endCond():
    global iterCount
    iterCount += 1
    return True if iterCount >= ITERATIONS else False


random.seed(42)
pop, best, bestFit = geneticAlgorithm(POP_SIZE, SELECT_SIZE, OBJ_SIZE,
                                      fitnessFunc, geneFunc, MUTATION_RATE, endCond)
print("Target:", TARGET_SECUENCE)
print("Best:  ", best)
print("Best fitness:", bestFit)

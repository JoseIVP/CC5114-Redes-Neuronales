from g_algorithm import geneticAlgorithm
import random

TARGET_SECUENCE = "helloworld"
OBJ_SIZE = len(TARGET_SECUENCE)
POP_SIZE = 20
SELECT_SIZE = 5
MUTATION_RATE = 0.1
ITERATIONS = 50
iterCount = 0


def geneFunc():
    # Retorna un caracter entre a y z
    return chr(96 + random.randint(1, 26))


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
                                      fitnessFunc, geneFunc, MUTATION_RATE, endCond, elitism=True)
print("Target:", TARGET_SECUENCE)
print("Best:  ", "".join(best))
print("Best fitness:", bestFit)

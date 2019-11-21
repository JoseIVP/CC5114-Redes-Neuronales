from g_algorithm import g_algorithm
from generator import Generator
from trees import binary_operation_node, value_node
import random


TARGET = 65346
POP_SIZE = 50
SELECT_SIZE = 5
MUTATION_RATE = 0.2
ITERATIONS = 400

SumNode = binary_operation_node(lambda a, b: a + b)
DifferenceNode = binary_operation_node(lambda a, b: a - b)
MultiplicationNode = binary_operation_node(lambda a, b: a * b)

internals = [SumNode, DifferenceNode, MultiplicationNode]
terminals = []

for n in [25, 7, 8, 100, 4, 2]:
    terminals.append(value_node(lambda: n))

fitness_records = ([], [], [])

generator = Generator(internals, terminals, depth=10, terminal_prob=0.3)


def fitness_func(root):
    return TARGET - abs(TARGET - root.eval())


iteration_count = 0


def end_condition():
    global iteration_count
    iteration_count += 1
    if iteration_count >= ITERATIONS:
        iteration_count = 0
        return True
    return False


_, _, best_fitness = g_algorithm(POP_SIZE, SELECT_SIZE, fitness_func, generator,
                                internals, terminals, MUTATION_RATE,
                                end_condition, elitism=True,
                                fitness_records=fitness_records)

print(best_fitness)

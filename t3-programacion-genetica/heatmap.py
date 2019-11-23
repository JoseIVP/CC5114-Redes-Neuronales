from g_algorithm import g_algorithm
from generator import Generator
from trees import binary_operation_node, value_node
import random
import matplotlib.pyplot as plt

TARGET = 65346
SEED = 7654547
ITERATIONS = 50

SumNode = binary_operation_node(lambda a, b: a + b)
DifferenceNode = binary_operation_node(lambda a, b: a - b)
MultiplicationNode = binary_operation_node(lambda a, b: a * b)
MaxNode = binary_operation_node(lambda a, b: max(a, b))

internals = [SumNode, DifferenceNode, MultiplicationNode, MaxNode]
terminals = []

for n in [25, 7, 8, 100, 4, 2]:
    terminals.append(value_node(lambda: n))

fitness_records = ([], [], [])  # mínimos, promedios y máximos

generator = Generator(internals, terminals, depth=3, terminal_prob=0.4)


def fitness_func(root):
    return TARGET / (1 + abs(TARGET - root.eval()))


iteration_count = 0


def end_condition():
    global iteration_count
    iteration_count += 1
    if iteration_count >= ITERATIONS:
        iteration_count = 0
        return True
    return False


population = [i for i in range(50, 1001, 50)]
mutation_rate = [i/10 for i in range(11)]
heatmap = []

random.seed(SEED)

for mut in mutation_rate:
    row = []
    for pop in population:
        select_size = 5
        _, _, best_fit = g_algorithm(pop, select_size, fitness_func, generator,
                                 internals, terminals, mut,
                                 end_condition, elitism=True)
        row.append(best_fit)
    heatmap.append(row)

fig, configs_plot = plt.subplots()
im = configs_plot.imshow(heatmap)

configs_plot.set_xticks([i for i in range(len(population))])
configs_plot.set_yticks([i for i in range(len(mutation_rate))])
configs_plot.set_yticklabels(mutation_rate)
configs_plot.set_xticklabels(population)
configs_plot.set(xlabel='Población', ylabel='Mutation rate',
                title="Heatmap de fitness para distintas configuraciones")
fig.tight_layout()
plt.show()
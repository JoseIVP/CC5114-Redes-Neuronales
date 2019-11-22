from g_algorithm import g_algorithm
from generator import Generator
from trees import binary_operation_node, value_node, AbstractTerminal
import random
import matplotlib.pyplot as plt


def count_nodes(node):
    if node.is_terminal():
        return 1
    left_count = count_nodes(node.children['left'])
    right_count = count_nodes(node.children['right'])
    return 1 + left_count + right_count


# ======================== 2.1 Encontrar Número ============================= #

# 2.1.1 Sin límite de repeticiones:

TARGET = 65346
POP_SIZE = 100
SELECT_SIZE = 10
MUTATION_RATE = 0.2
ITERATIONS = 400

SumNode = binary_operation_node(lambda a, b: a + b)
DifferenceNode = binary_operation_node(lambda a, b: a - b)
MultiplicationNode = binary_operation_node(lambda a, b: a * b)

internals = [SumNode, DifferenceNode, MultiplicationNode]
terminals = []

for n in [25, 7, 8, 100, 4, 2]:
    terminals.append(value_node(lambda: n))

fitness_records = ([], [], [])  # mínimos, promedios y máximos

generator = Generator(internals, terminals, depth=10, terminal_prob=0.3)


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


""" random.seed(7654547)
_, best_obj, best_fitness = g_algorithm(POP_SIZE, SELECT_SIZE, fitness_func, generator,
                                 internals, terminals, MUTATION_RATE,
                                 end_condition, elitism=True,
                                 fitness_records=fitness_records)


print('Sin límite de repeticiones:')
print('\tMejor fitness:', best_fitness)
print('\tSolución:', best_obj.eval())
print('\tCantidad de nodos:', count_nodes(best_obj))
x = [i for i in range(1, ITERATIONS + 1)]
_, fitness_plot = plt.subplots()
for y in fitness_records:
    fitness_plot.plot(x, y)
fitness_plot.legend(['Peor', 'Promedio', 'Mejor'])
fitness_plot.set(xlabel='Generación', ylabel='Fitness',
                title='Fitness por generación para valores con repetición') """


# 2.1.2 Fitness:

def fitness_func_size(root):
    return TARGET / abs(TARGET - root.eval()) - 0.01 * count_nodes(root)


fitness_records = ([], [], [])  # mínimos, promedios y máximos

""" random.seed(7654547)
_, best_obj, best_fitness = g_algorithm(POP_SIZE, SELECT_SIZE, fitness_func_size, generator,
                                internals, terminals, MUTATION_RATE,
                                end_condition, elitism=True,
                                fitness_records=fitness_records)


print('\nFitness castigando árboles grandes:')
print('\tMejor fitness:', best_fitness)
print('\tSolución:', best_obj.eval())
print('\tCantidad de nodos:', count_nodes(best_obj))
x = [i for i in range(1, ITERATIONS + 1)]
_, fitness_plot = plt.subplots()
for y in fitness_records:
    fitness_plot.plot(x, y)
fitness_plot.legend(['Peor', 'Promedio', 'Mejor'])
fitness_plot.set(xlabel='Generación', ylabel='Fitness',
                title='Fitness por generación con castigo por tamaño')
plt.show() """


# 2.1.3 Sin repetición:

def repeats_nodes(node, terminals_dic):
    if node.is_terminal():
        terminals_dic[type(node)] += 1
        if terminals_dic[type(node)] > 1:
            return True
        return False
    return repeats_nodes(node.children['left'], terminals_dic) or \
        repeats_nodes(node.children['right'], terminals_dic)


def fitness_func_repeat(root):
    nodes_dic = {}
    for node_class in terminals:
        nodes_dic[node_class] = 0
    if repeats_nodes(root, nodes_dic):
        return 0
    return TARGET / abs(TARGET - root.eval())

fitness_records = ([], [], [])  # mínimos, promedios y máximos
generator = Generator(internals, terminals, depth=4, terminal_prob=0.4)

""" random.seed(7654547)
_, best_obj, best_fitness = g_algorithm(POP_SIZE, SELECT_SIZE, fitness_func_repeat, generator,
                                internals, terminals, MUTATION_RATE,
                                end_condition, elitism=True,
                                fitness_records=fitness_records)

print('\nFitness castigando repetición:')
print('\tMejor fitness:', best_fitness)
print('\tSolución:', best_obj.eval())
print('\tCantidad de nodos:', count_nodes(best_obj))
x = [i for i in range(1, ITERATIONS + 1)]
_, fitness_plot = plt.subplots()
for y in fitness_records:
    fitness_plot.plot(x, y)
fitness_plot.legend(['Peor', 'Promedio', 'Mejor'])
fitness_plot.set(xlabel='Generación', ylabel='Fitness',
                title='Fitness por generación castigando repetición de terminales')
plt.show()  """


# 2.2 Implementar variables:

class VariableNode(AbstractTerminal):

    def __init__(self, parent=None, key=None):
        super().__init__(None, parent=parent, key=key)

    def eval(self, var_dic={}):
        return var_dic[type(self)]


# 2.3 Symbolic Regression:

POP_SIZE = 100
SELECT_SIZE = 10
MUTATION_RATE = 0.2
ITERATIONS = 400

terminals = [VariableNode]
generator = Generator(internals, terminals, depth=10, terminal_prob=0.3)

for n in range(-10, 11):
    terminals.append(value_node(lambda: n))


def fitness_func_regression(node):
    error = 0
    for x in range(-100, 101):
        target = x**2 + x - 6
        var_dic = {}
        var_dic[VariableNode] = x
        error += abs(node.eval(var_dic=var_dic) - target)
    return 1 / error


random.seed(7654547)
_, best_obj, best_fitness = g_algorithm(POP_SIZE, SELECT_SIZE, fitness_func_regression, generator,
                                         internals, terminals, MUTATION_RATE,
                                         end_condition, elitism=True,
                                         fitness_records=fitness_records)

print('\nSymbolic Regression:')
print('\tMejor fitness:', best_fitness)
print('\tCantidad de nodos:', count_nodes(best_obj))
x = [i for i in range(1, ITERATIONS + 1)]
_, fitness_plot = plt.subplots()
for y in fitness_records:
    fitness_plot.plot(x, y)
fitness_plot.legend(['Peor', 'Promedio', 'Mejor'])
fitness_plot.set(xlabel='Generación', ylabel='Fitness',
                title='Fitness por generación para Symbolic Regression')


_, regression_plot = plt.subplots()
x = [i for i in range(-100, 101)]
y = [i**2 + i - 6 for i in x]
y_regression = []
for i in x:
    y_regression.append(best_obj.eval(var_dic={VariableNode: i}))
regression_plot.plot(x, y)
regression_plot.plot(x, y_regression)
regression_plot.legend(['Real', 'Symbolic Regression'])
regression_plot.set(xlabel='x', ylabel='y',
                title='Comparación de x**2 + x - 6 vs Symbolic Regression')
plt.show()

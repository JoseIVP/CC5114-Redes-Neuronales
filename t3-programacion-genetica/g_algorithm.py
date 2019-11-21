from generator import Generator
import random


def crossover(selection: list):
    # Randomly select 2 roots.
    root1 = selection[random.randint(0, len(selection) - 1)]
    root2 = selection[random.randint(0, len(selection) - 1)]
    root1_copy = root1.copy()
    root2_copy = root2.copy()

    # Get the list of nodes for each root.
    node_list1 = []
    node_list2 = []
    root1_copy.serialize(node_list1)
    root2_copy.serialize(node_list2)

    # Randomly select the nodes to be swapped.
    p1 = node_list1[random.randint(0, len(node_list1) - 1)]
    p2 = node_list2[random.randint(0, len(node_list2) - 1)]

    # Swap the parents and keys of the two nodes.
    p1.parent, p2.parent = p2.parent, p1.parent
    p1.key, p2.key = p2.key, p1.key

    # Set the corresponding child for each parent.
    if p1.parent != None:
        p1.parent.children[p1.key] = p1
    if p2.parent != None:
        p2.parent.children[p2.key] = p2

    return root1_copy, root2_copy


def mutate(root, mutation_rate: float, internals: list, terminals: list):
    node_list = []
    root.serialize(node_list)
    for node in node_list:
        if random.random() < mutation_rate:
            parent = node.parent
            key = node.key
            if node.is_terminal():
                new_node = terminals[random.randint(
                    0, len(terminals) - 1)](parent=parent, key=key)
            else:
                new_node = internals[random.randint(0, len(internals) - 1)](parent=parent, key=key,
                                                                            **node.children)

            if parent != None:
                parent.children[key] = new_node
            
            if node == root:
                root = new_node
    return root
    

def g_algorithm(pop_size: int, select_size: int, fitness_func,
                generator: Generator, internals: list, terminals: list,
                mutation_rate: float, end_condition,
                elitism: bool = False, fitness_records: tuple = None):

    population = [generator.generate() for _ in range(pop_size)]
    
    while True:
        fitness = []
        best_obj, best_fitness = None, 0
        for obj in population:
            fitness.append(fitness_func(obj))
            if fitness[-1] >= best_fitness:
                best_obj = obj
                best_fitness = fitness[-1]

        # Calculate accumulative fitness
        fitness_acc = [(fitness[i] + (0 if i == 0 else fitness[i-1]))
                       for i in range(pop_size)]

        if fitness_records != None:
            # fitnessRecords is expected to be a 3-tuple of lists.
            fitness_records[0].append(min(fitness))
            fitness_records[1].append(fitness_acc[-1] / pop_size)
            fitness_records[2].append(best_fitness)
        
        if end_condition():
            break

        # Roulette selection:
        selection = []
        rands = [random.random() * fitness_acc[-1] for _ in range(select_size)]
        rands.sort()
        j = 0
        for r in rands:
            while fitness_acc[j] < r:
                j += 1
            selection.append(population[j])

        new_pop_size = pop_size - 1 if elitism else pop_size

        # Crossover:
        population = []
        for _ in range(int(new_pop_size/2)):
            obj1, obj2 = crossover(selection)
            population.append(obj1)
            population.append(obj2)

        if new_pop_size % 2 != 0:
            obj1, _ = crossover(selection)
            population.append(obj1)

        # Mutation:
        for i in range(new_pop_size):
            population[i] = mutate(population[i], mutation_rate, internals, terminals)

        if elitism:
            population.append(best_obj)

    return population, best_obj, best_fitness

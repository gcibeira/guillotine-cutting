import random


def generate_random_chromosome(n):
    parts = list(range(1, n + 1))
    random.shuffle(parts)
    genes = []
    count = 0

    for _ in range(len(parts) * 2 - 1):
        if count < 2:
            genes.append(parts.pop())
            count += 1
        else:
            if len(parts) == 0:
                genes.append(random.choice(["H", "V"]))
            elif random.choice([True, False]):
                genes.append(parts.pop())
                count += 1
            else:
                genes.append(random.choice(["H", "V"]))
                count -= 1

    return genes


def mutate_genes(genes):
    mutant = genes.copy()

    # Select two random positions in the genes
    point1, point2 = sorted(random.sample(range(len(mutant)), 2))

    # Ensure position1 is located to the left of position2
    if point1 > point2:
        point1, point2 = point2, point1

    # Get the elements at the selected positions
    element1 = mutant[point1]
    element2 = mutant[point2]

    # If both elements are part numbers, swap them
    if isinstance(element1, int) and isinstance(element2, int):
        mutant[point1], mutant[point2] = element2, element1

    # If element1 is a part number and element2 is an operator, check if swapping is allowed
    elif isinstance(element1, int) and isinstance(element2, str):
        mutant[point2] = "H" if mutant[point2] == "V" else "V"

    # If element1 is an operator, swap them without condition
    elif isinstance(element1, str):
        if element1 != element2:
            mutant[point1], mutant[point2] = element2, element1
        else:
            mutant[point1] = "H" if mutant[point1] == "V" else "V"

    return mutant


def check_operator_swap_condition(genes, point):
    # Check if the condition for swapping operators is satisfied
    np = 0
    no = 0

    for i in range(point):
        if isinstance(genes[i], int):
            np += 1
        else:
            no += 1

    return no <= np - 2


def pmx_crossover(parent1, parent2):
    # Step 2: Randomly select crossover points
    items1 = get_items(parent1)
    items2 = get_items(parent2)
    point1, point2 = sorted(random.sample(range(len(items1)), 2))

    # Step 3: Copy the segment between the crossover points
    child1 = [None] * len(items1)
    child1[point1:point2] = items1[point1:point2]

    # Step 4: Fill in missing genes using parent2
    for i in range(len(items1)):
        if point1 <= i < point2:
            continue  # This segment is already copied from parent1

        gene = items2[i]
        while gene in child1:
            index = items2.index(gene)
            gene = items1[index]

        child1[i] = gene

    # Step 3: Copy the segment between the crossover points
    child2 = [None] * len(items2)
    child2[point1:point2] = items2[point1:point2]

    # Step 4: Fill in missing genes using parent2
    for i in range(len(items2)):
        if point1 <= i < point2:
            continue  # This segment is already copied from parent1

        gene = items1[i]
        while gene in child2:
            index = items1.index(gene)
            gene = items2[index]

        child2[i] = gene

    child1 = merge_items(parent1, child1)
    child2 = merge_items(parent2, child2)
    return child1, child2


def get_items(genes):
    return [item for item in genes if isinstance(item, int)]


def merge_items(genes, items):
    reconstructed = []
    for gen in genes:
        if isinstance(gen, int):
            reconstructed.append(items.pop(0))
        else:
            reconstructed.append(gen)
    return reconstructed


def fitness(genes, items):
    stack = []

    for gene in genes:
        if isinstance(gene, int):
            stack.append(items[int(gene) - 1])
        elif gene == "H":
            item2 = stack.pop()
            item1 = stack.pop()
            stack.append((item1[0] + item2[0], max(item1[1], item2[1])))
        elif gene == "V":
            item2 = stack.pop()
            item1 = stack.pop()
            stack.append((max(item1[0], item2[0]), item1[1] + item2[1]))

    if len(stack) != 1:
        raise ValueError(
            "Invalid layout genes. The stack should contain a single root node."
        )

    # The top of the stack represents the final integrated rectangle
    fitness = stack[0][0] * stack[0][1]
    return fitness

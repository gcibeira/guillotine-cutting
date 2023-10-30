from layout import create_layout, load_nodes
import random


def generate_random_chromosome(nodes):
    random.shuffle(nodes)
    genes = []
    count = 0

    for _ in range(len(nodes) * 2 - 1):
        if count < 2:
            genes.append(nodes.pop())
            count += 1
        else:
            if len(nodes) == 0:
                genes.append(random.choice(["H", "V"]))
            elif random.choice([True, False]):
                genes.append(nodes.pop())
                count += 1
            else:
                genes.append(random.choice(["H", "V"]))
                count -= 1

    return genes


if __name__ == "__main__":
    nodes = load_nodes("items.csv")
    chromosome = generate_random_chromosome(nodes)
    root = create_layout(chromosome)
    root.plot()

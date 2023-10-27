from layout import Node
import csv
import random


def load_nodes_from_csv(file_path):
    nodes = []
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            width = int(row["Width"])
            height = int(row["Height"])
            node = Node(width, height)
            nodes.append(node)
    return nodes


def generate_genes(count):
    parts = list(range(1, count + 1))
    random.shuffle(parts)
    genes = []
    flag = 0

    for _ in range(count * 2 - 1):
        if flag < 2:
            genes.append(parts.pop())
            flag += 1
        else:
            if len(parts) == 0:
                genes.append(random.choice(["H", "V"]))
            elif random.choice([True, False]):
                genes.append(parts.pop())
                flag += 1
            else:
                genes.append(random.choice(["H", "V"]))
                flag -= 1

    return genes


def create_layout(genes, nodes):
    stack = []

    for gene in genes:
        if isinstance(gene, int):
            node = nodes[int(gene) - 1]
            stack.append(node)
        elif gene == "H":
            # Horizontal operation: Combine two parts horizontally
            node2 = stack.pop()
            node1 = stack.pop()
            combined_node = node1.combine(node2, is_horizontal=True)
            stack.append(combined_node)
        elif gene == "V":
            # Vertical operation: Combine two parts vertically
            node2 = stack.pop()
            node1 = stack.pop()
            combined_node = node1.combine(node2, is_horizontal=False)
            stack.append(combined_node)

    if len(stack) != 1:
        raise ValueError(
            "Invalid layout genes. The stack should contain a single root node."
        )

    # The top of the stack represents the final integrated rectangle
    return stack[0]


if __name__ == "__main__":
    nodes = load_nodes_from_csv("items.csv")
    genes = generate_genes(len(nodes))
    print(genes)
    # genes = [1, 5, "H", 7, 6, "V", 2, "H", 4, "H", "V", 9, 8, "V", 3, "V", "H"]
    root = create_layout(genes, nodes)
    print(f"Total: {root.width}x{root.height}")
    root.plot()

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv


class Node:
    def __init__(self, width, height, is_horizontal=False):
        self.width = width
        self.height = height
        self.is_horizontal = is_horizontal
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def combine(self, other_node, is_horizontal=True):
        if is_horizontal:
            # Combine horizontally
            combined_width = self.width + other_node.width
            combined_height = max(self.height, other_node.height)
        else:
            # Combine vertically
            combined_width = max(self.width, other_node.width)
            combined_height = self.height + other_node.height

        combined_node = Node(combined_width, combined_height, is_horizontal)
        combined_node.add_child(self)
        combined_node.add_child(other_node)

        return combined_node

    def is_leaf(self):
        return not self.children

    def plot(self):
        fig, ax = plt.subplots()
        ax.text(
            self.width / 2,
            self.height,
            f"{self.width}x{self.height}",
            ha="center",
            color="black",
        )
        self.subplot(ax)
        ax.set_aspect("equal")
        ax.autoscale_view()
        plt.show()

    def subplot(self, ax, x=0, y=0):
        if self.is_leaf():
            # Plot the leaf node as a rectangle
            rect = Rectangle((x, y), self.width, self.height, color="red", fill=None)
            ax.add_patch(rect)
            # Add text label inside the rectangle to identify the node
            ax.text(
                x + self.width / 2,
                y + self.height / 2,
                f"{self.width}x{self.height}",
                ha="center",
                va="center",
                color="black",
            )
        else:
            rect = Rectangle(
                (x, y),
                self.width,
                self.height,
                color="blue",
                fill=None,
                alpha=0.5,
                linestyle="dashed",
            )
            ax.add_patch(rect)
            # Recursively plot the children
            if self.is_horizontal:
                # Horizontal combination
                x_offset = 0
                for child in self.children:
                    child.subplot(ax, x + x_offset, y)
                    x_offset += child.width
            else:
                # Vertical combination
                y_offset = 0
                for child in self.children:
                    child.subplot(ax, x, y + y_offset)
                    y_offset += child.height


def load_nodes(file_path):
    nodes = []
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            width = int(row["Width"])
            height = int(row["Height"])
            node = Node(width, height)
            nodes.append(node)
    return nodes


# Creates a layout from a chromosome representation
def create_layout(genes):
    stack = []

    for gene in genes:
        if isinstance(gene, Node):
            stack.append(gene)
        elif gene == "H":
            node2 = stack.pop()
            node1 = stack.pop()
            combined_node = node1.combine(node2, is_horizontal=True)
            stack.append(combined_node)
        elif gene == "V":
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

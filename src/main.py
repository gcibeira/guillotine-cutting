from data_loader import load_items  # Load item data
from ga import genetic_algorithm, fitness  # Genetic algorithm and fitness function
from layout import create_layout, load_nodes  # Create layout and load nodes
import argparse


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Genetic Algorithm for 2D Layout Optimization"
    )
    parser.add_argument("csv_file", help="path to CSV file containing item data")
    args = parser.parse_args()

    # Load item data from the specified CSV file
    items = load_items(args.csv_file)

    # Define genetic algorithm parameters
    population_size = 5000
    chromosome_length = len(items)
    generations = 100
    elite_size = 3
    mutation_rate = 0.2

    # Run the genetic algorithm to find the best layout
    best_individual = genetic_algorithm(
        population_size,
        chromosome_length,
        generations,
        elite_size,
        mutation_rate,
        items,
    )

    # Calculate the fitness (total area needed) of the best layout
    best_fitness = fitness(best_individual, items)

    # Print the best individual and its fitness
    print("Best Individual:", best_individual)
    print("Best Fitness (Total Area Needed):", best_fitness)

    # Load nodes for creating the layout
    nodes = load_nodes("items.csv")

    # Create and plot the layout based on the best individual
    layout = create_layout(best_individual, nodes)
    layout.plot()

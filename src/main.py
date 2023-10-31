from ga import generate_random_chromosome, fitness, pmx_crossover, mutate_genes
from layout import create_layout, load_nodes
import csv
import random
import matplotlib.pyplot as plt


best_fitness_values = []


# Function to initialize the population with random individuals
def initialize_population(population_size, chromosome_length):
    population = [
        generate_random_chromosome(chromosome_length) for _ in range(population_size)
    ]
    return population


# Function to select the top 'elite_size' individuals from the population
def select_elite(population, elite_size, items):
    population_with_fitness = [
        (individual, fitness(individual, items)) for individual in population
    ]
    sorted_population = sorted(population_with_fitness, key=lambda x: x[1])
    best_fitness_values.append(population_with_fitness[0][1])
    elite = [individual for individual, _ in sorted_population[:elite_size]]
    return elite


# Genetic Algorithm
def genetic_algorithm(
    population_size, chromosome_length, generations, elite_size, mutation_rate, items
):
    # Initialize the population
    population = initialize_population(population_size, chromosome_length)

    for _ in range(generations):
        # Select the elite individuals
        elite = select_elite(population, elite_size, items)

        # Create a new population with the elite individuals
        new_population = elite[:]

        # Fill the rest of the new population
        while len(new_population) < population_size:
            # Perform selection and crossover
            parent1, parent2 = random.choices(population, k=2)
            child1, child2 = pmx_crossover(parent1, parent2)

            # Perform mutation
            if random.random() < mutation_rate:
                child1 = mutate_genes(child1)
            if random.random() < mutation_rate:
                child2 = mutate_genes(child2)

            # Add the children to the new population
            new_population.extend([child1, child2])

        # Update the population with the new population
        population = new_population

    # Select and return the best individual from the final population
    best_individual, _ = min(
        [(individual, fitness(individual, items)) for individual in population],
        key=lambda x: x[1],
    )
    return best_individual


def load_items(file_path):
    items = []
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            width = int(row["Width"])
            height = int(row["Height"])
            item = (width, height)
            items.append(item)
    return items


if __name__ == "__main__":
    items = load_items("items.csv")
    population_size = 5000
    chromosome_length = len(items)
    generations = 100
    elite_size = 3
    mutation_rate = 0.2

    best_individual = genetic_algorithm(
        population_size,
        chromosome_length,
        generations,
        elite_size,
        mutation_rate,
        items,
    )
    best_fitness = fitness(best_individual, items)

    print("Best Individual:", best_individual)
    print("Best Fitness (Total Area Needed):", best_fitness)

    nodes = load_nodes("items.csv")
    layout = create_layout(best_individual, nodes)
    layout.plot()

    # Plot a graph to visualize the progress
    plt.figure(figsize=(10, 6))
    plt.plot(range(generations), best_fitness_values, label="Best Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.title("Genetic Algorithm Progress")
    plt.grid(True)
    plt.show()

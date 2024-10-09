import numpy as np
from Maze import Maze
from enum import Enum
import random


class Direction(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3


class Genetic_algorithm:
    # Define the fitness function

    # Define the GA parameters
    _population_size = 100
    _num_generations = 50
    _mutation_rate = 0.1
    _crossover_rate = 0.7
    _population: list
    _maze: Maze
    _growth_rate: float

    # Initialize the population
    def __init__(
        self,
        maze: Maze,
        population_size: int,
        num_generations: int,
        mutation_rate: int,
        crossover_rate: int,
        growth_rate: float = 0.5
    ):
        self._maze = maze
        self._population_size = population_size
        self._num_generations = num_generations
        self._mutation_rate = mutation_rate
        self._crossover_rate = crossover_rate
        self._population = list()
        self._growth_rate = growth_rate

        for i in range(population_size):
            self._population.append([Direction(random.randint(0, 3)) for _ in range(2)])

    def get_position(self, individual):
        for direction in individual:
            x, y = self._maze.START
            match direction:
                case Direction.Up:
                    y -= 2
                case Direction.Down:
                    y += 2
                case Direction.Left:
                    x -= 2
                case Direction.Right:
                    x += 2
        return x, y

    def fitness_function(self, individual: list[Direction]) -> int:
        x, y = self._maze.START
        length = 0
        has_visited = []
        for direction in individual:
            y_inc = 0
            x_inc = 0
            has_visited.append((x, y))
            length += 1
            match direction:
                case Direction.Up:
                    y_inc = -1
                case Direction.Down:
                    y_inc = 1
                case Direction.Left:
                    x_inc = -1
                case Direction.Right:
                    x_inc = 1

            if self._maze.is_wall(x + x_inc, y + y_inc) or (x + x_inc * 2, y + y_inc * 2) in has_visited:
                return 1
            x += x_inc * 2
            y += y_inc * 2

        distance_to_goal = (
            abs(self._maze._GOAL[0] - x) // 2 + abs(self._maze._GOAL[1] - y) // 2
        )
        if distance_to_goal == 0:
            return 1000000
        return 300 - distance_to_goal * 5 - length

    # Evaluate the population
    def evaluate_population(self, population):
        fitness_values = []
        for individual in population:
            fitness = self.fitness_function(individual)
            fitness_values.append(fitness)
        return fitness_values

    # Select parents using roulette wheel selection
    def select_parents(self, population, fitness_values):
        fitness_values = np.array(fitness_values)
        # Ensure non-negative fitness values for selection
        fitness_values = np.maximum(fitness_values, 0)
        total_fitness = fitness_values.sum()

        if total_fitness <= 0:
            raise ValueError("Total fitness is non-positive; check fitness function.")

        probabilities = fitness_values / total_fitness
        indices = np.arange(len(population))
        parents = np.random.choice(indices, size=len(population), p=probabilities)
        return [population[i][:] for i in parents]

    # Perform crossover between two parents
    def crossover(self, parent1: list, parent2: list):
        if np.random.rand() < self._crossover_rate:
            min_length = min(len(parent1), len(parent2))
            alpha = np.random.randint(0, min_length - 1)
            child1 = parent1[:alpha] + parent2[alpha:]
            child2 = parent2[:alpha] + parent1[alpha:]
            return child1, child2
        else:
            return parent1, parent2

    # Perform mutation on an individual
    def mutate(self, individual: list):
        if np.random.rand() < self._mutation_rate:
            gene = np.random.randint(0, len(individual) - 1)
            individual[gene] = np.random.choice(Direction)
        if np.random.rand() < self._growth_rate:
            individual.append(Direction(random.randint(0, 3)))
        return individual

    # Main GA function
    def run(self):
        best_individuals_per_gen = []
        for generation in range(self._num_generations):
            fitness_values = self.evaluate_population(self._population)
            self._population = self.select_parents(self._population, fitness_values)

            new_population = []
            for i in range(0, self._population_size, 2):
                parent1 = self._population[i]
                parent2 = self._population[i + 1]
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))
            self._population = new_population

            best_individual = max(
                self._population, key=lambda ind: self.fitness_function(ind)
            )
            best_fitness = self.fitness_function(best_individual)
            best_individuals_per_gen.append(best_individual)
            if best_fitness > 1000:
                return best_individuals_per_gen

        return best_individuals_per_gen

    # Run the GA

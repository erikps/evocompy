import csv

import numpy as np

class EvolutionSettings:
    """ General evolution settings. """
    def __init__(self, population_size, mutation_probability):
        self.population_size = population_size
        self.mutation_probability = mutation_probability
    
    def __repr__(self):
        return f"pop={self.population_size} mprob={self.mutation_probability}"

class Evolution:
    """ Implementation of an evolutionary algorithm that removes the need for boilerplate code. """
    def __init__(self, settings, random_function, fitness_function, mutation_function, crossover_function=lambda x: x, proportional=True):
        self.population_size = settings.population_size
        self.mutation_probability = settings.mutation_probability
        self.random_function = random_function
        self.fitness_function = fitness_function
        self.mutation_function = mutation_function
        self.crossover_function = crossover_function
        self.proportional = proportional
        self.current_population = self._generate_initial_population()
        self.current_fitness_values = []
        self._compute_fitness_values()

    def step(self):
        """ Generates the next population. """
        self.current_population = self._generate_next_population()
        self._compute_fitness_values()

    def get_fittest_individual(self):
        """ Returns a 2-tuple with the fittest individual and its fitness value. """
        fittest = max(self.current_population, key=self.fitness_function) if self.proportional else min(self.current_population, key=self.fitness_function)
        return (fittest, self.fitness_function(fittest))
    
    def get_mean_fitness(self):
        """ Computes the mean fitness of the current population. """
        return np.mean(self.current_fitness_values)

    def get_median_fitness(self):
        """ Computes the median fitness of the current population. """        
        return np.median(self.current_fitness_values)
    
    def _compute_fitness_values(self):
        self.current_fitness_values = np.array(list(map(self.fitness_function, self.current_population)))

    def _generate_initial_population(self):
        initial_population = []
        for _ in range(self.population_size):
            initial_population.append(self.random_function())
        return np.array(initial_population)

    def _generate_next_population(self):
        next_population = []
        selected_population = sorted(self.current_population, key=self.fitness_function, reverse=not self.proportional)[int(len(self.current_population)/2):]
        for i, _ in enumerate(self.current_population):
            next_population.append(self.crossover_function(self.mutation_function(selected_population[i%len(selected_population)])))
        return np.array(next_population)

def settings_from_file(path):
    settings = []
    with open(path) as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        for row in reader:
            settings.append(EvolutionSettings(float(row[0]), int(row[1])))
    return settings 

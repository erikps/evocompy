import csv
import random

import numpy as np

class Evolution:
    """ Implementation of an evolutionary algorithm that removes the need for boilerplate code. """
    def __init__(self, population_size, random_function, fitness_function, selection_scheme, genetic_operators, proportional=True, writer=None):
        self.population_size = population_size
        self.random_function = random_function
        self.fitness_function = fitness_function
        self.selection_scheme = selection_scheme
        self.genetic_operators = genetic_operators
        
        self.proportional = proportional
        self.writer = writer

        self.generation = 0

        self.current_population = self._generate_initial_population()
        self.current_fitness_values = []
        self._compute_fitness_values()
        self._write_to_writer()

    def step(self):
        """ Generates the next population. """
        self.current_population = self._generate_next_population()
        self._compute_fitness_values()
        self._write_to_writer()
        self.generation += 1

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
    
    def finalize_writer(self):
        """ Calls the finalize method of the used writer, if there is one. """
        if self.writer is not None:
            self.writer.finalize()

    def _compute_fitness_values(self):
        self.current_fitness_values = np.array(list(map(self.fitness_function, self.current_population)))

    def _generate_initial_population(self):
        initial_population = []
        for _ in range(self.population_size):
            individual = self.random_function()
            initial_population.append(individual)
        return np.array(initial_population)

    def _generate_next_population(self):
        next_population = self.selection_scheme(self.current_population, self.fitness_function, self.proportional)
        for operator in self.genetic_operators:
            next_population = operator(next_population, self.population_size)
        return np.array(next_population)

    def _write_to_writer(self):
        if self.writer is not None:
            self.writer.step(self)


# Selection Methods:

def cutoff_selection(population, f, proportional):
    """ Simple and naive selection method that simply cuts of the lower half of the population ordered by fitness. """
    selected = list(
        sorted(population, key=f, reverse=not proportional
        )[int(len(population)/2):])
    new_pop = []
    for i, _ in enumerate(population):
        new_pop.append(selected[i%len(selected)])
    return np.array(new_pop)


def roulette_wheel_selection(population, f, proportional):
    """ Implementation of the roulette wheel selection method. """
    S = sum(map(f, population))
    new_population = []
    for _ in population:
        alpha, iSum = random.uniform(0, S), 0
        chosen = None
        for individual2 in population:
            iSum += f(individual2)
            chosen = individual2
            if iSum >= alpha:
                break
        new_population.append(chosen)
    return np.array(new_population)


def roulette_wheel_selection_orig(population, f, proportional):
    """ Implementation of the roulette wheel selection method. """
    S = sum(map(f, population))
    new_population = []
    for _ in population:
        alpha, iSum = random.uniform(0, S), 0
        chosen = None
        for individual2 in population:
            iSum += f(individual2)
            chosen = individual2
            if iSum >= alpha:
                break
        new_population.append(chosen)

    return np.array(new_population)

# Genetic Operator Decorators:

def mutation_operator(m):
    """ Decorator that takes the mutation function f and turns it into a genetic operator. 
        A mutation function is applied to each individual separately.
    """
    def result(pop, pop_size):
        return np.array(list(map(m, pop)))
    return result

def crossover_operator(f, sort=True, **kwargs):
    """ Decorator that takes a function operating on two chromosomes and turns it into a proper genetic operator. 
        It refills the selected population to the required population size. There is no sexual selection simulated, 
        all surviving individuals are equally as likely to reproduce, no matter their respective fitness scores.
    """
    def result(sorted_population, population_size):
        population = sorted_population
        new_population = []
        if not sort: 
            random.shuffle(population)
        length = len(population)
        for i in range(population_size):
            new_population.append(f(i%length, (i+1)%length)) 
    return result
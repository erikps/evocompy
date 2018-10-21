import math
import csv
import random

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm, colors, ticker, style

from .evolution import Evolution, EvolutionSettings

class Evolution2DSettings(EvolutionSettings):
    def __init__(self, distribution, population_size, mutation_probability):
        super().__init__(population_size, mutation_probability)
        self.distribution = distribution

    def __repr__(self):
        return super().__repr__() + f""

class Evolution2D:
    """ Evolution2D is a wrapper for the Evolution class that allows the creation of an evolutionary algorithm for 2 dimensional functions. """
    def __init__ (self, function, settings, value_range, step):
        self.function = function
        self.settings = settings
        self.value_range = value_range
        self.step = step
        self.evolution = Evolution(settings, self.random, self.function, self.mutate)
        
    def random (self):
        """ Returns a random point within the value range. """
        return np.array([random.uniform(self.value_range[0], self.value_range[1]), random.uniform(self.value_range[0], self.value_range[1])])

    def mutate(self, individual):
        """ Returns a point that is clamped in the range but slightly mutated, between -mutation_max_step and mutation_max_step. """
        x = min(max(individual[0] + self.settings.distribution(), self.value_range[0]), self.value_range[1])
        y = min(max(individual[1] + self.settings.distribution(), self.value_range[0]), self.value_range[1])
        return np.array([x, y])

    def create_values(self):
        """ Creates and returns a tuple (X, Y, Z) of values. While X and Y are created based on the value range and step properties, Z is created by computing f([x, y])."""
        X = np.arange(self.value_range[0], self.value_range[1], self.step)
        Y = np.arange(self.value_range[0], self.value_range[1], self.step)
        Z = np.zeros((len(X), len(Y)))
        for ix, x in enumerate(X):
            for iy, y in enumerate(Y):
                Z[ix][iy] = self.function(np.array([x, y]))
        return (X, Y, Z)

def settings2d_from_file(path):
    """ Takes in a csv file containing settings for Function2DEvolution instances. Returns a list of Evolution2DSettings """
    settings = []
    with open(path) as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        for row in reader:
            settings.append(Evolution2DSettings(to_distribution(row[0]), int(row[1]), float(row[2])))
    return settings 

def to_distribution(string):
    class distribution:
        def __init__(self):   
            self.distribution_dict = {
                'uniform' : self.uniform,
                'normal' : self.normal,
            }

        def uniform(self, step):
            return lambda: random.uniform(-step, step)

        def normal(self, sigma):
            return lambda: random.normalvariate(0, sigma)
    distributions = distribution()
    split = string.split(' ')
    dist, value = split
    value = float(value)
    return distributions.distribution_dict[dist](value)
    

# Example Functions:

def sine(individual):
    """ Sine function using the sum of sin(x) and sin(y). The result is then multiplied by xy to create a falloff as xy approaches 0. """ 
    x, y = individual    
    value = (math.sin(x) + math.sin(y)) * x * y
    return max(0, value)

def parabola(individual):
    """ Parabola function of x squared plus y squared.  """
    x, y = individual
    return x*x + y*y


function_dict = {
    'sine' : sine,
    'parabola' : parabola,
}

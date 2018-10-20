import math
import csv
import random

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm, colors, ticker, style

from evolution import Evolution, EvolutionSettings

class Evolution2DSettings(EvolutionSettings):
    def __init__(self, mutation_max_step, population_size, mutation_probability):
        super().__init__(population_size, mutation_probability)
        self.mutation_max_step = mutation_max_step

    def __repr__(self):
        return super().__repr__() + f" mstep={self.mutation_max_step}"

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
        x = min(max(individual[0] + random.uniform(-self.settings.mutation_max_step, self.settings.mutation_max_step), self.value_range[0]), self.value_range[1])
        y = min(max(individual[1] + random.uniform(-self.settings.mutation_max_step, self.settings.mutation_max_step), self.value_range[0]), self.value_range[1])
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
    # TODO: This can be abstracted out, so it can be used for all evolutions, no matter the exact specification.
    """ Takes in a csv file containing settings for Function2DEvolution instances. Returns a list of Evolution2DSettings """
    settings = []
    with open(path) as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        for row in reader:
            settings.append(Evolution2DSettings(float(row[0]), int(row[1]), float(row[2])))
    return settings 



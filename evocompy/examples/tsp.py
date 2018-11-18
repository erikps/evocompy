"""
Usage:
    tsp.py <nodecount> <popsize> <mprob> <mnum> <outputfile>
"""
import csv
import random
    
import docopt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection


from ..evolution import Evolution, mutation_operator, cutoff_selection
from ..view import View
from ..io import CSVWriter


DIGITS = 2
COLOR = 'orange'

class TSP: 
    """ Implementation of the traveling salesperson problem. 
        A Solution is given as an array of indices corresponding to the nodes array indices.
    """
    def __init__(self, nodecount, coordinate_range=1):
        self.nodecount = nodecount
        self.coordinate_range = coordinate_range
        self.nodes = self._generate_nodes(nodecount)
        self.distances = self._generate_distances()        

    def random_solution(self):
        """ Returns a uniformly randomized solution for the tsp. """ 
        solution = np.arange(self.nodecount)
        np.random.shuffle(solution)
        return solution

    def get_distance(self, n1, n2):
        """ Returns the cost of a potential edge of the graph. Utilizes the underlying representation of the cost matrix as a dictionary. """
        return self.distances[n1, n2]

    def solution_cost(self, solution):
        """ Calculates the sum of all edges traversed in the given solution. """
        cost = 0
        for i in range(len(solution)):
            dist = self.get_distance(solution[i], solution[(i+1)%len(solution)])
            cost += dist  
        return cost

    def save_csv(self, filename):
        """ Serializes the TSP into a csv file. """
        

    def load_csv(self, filename):
        """ Deserializes a TSP from a given csv file. """

    def _generate_nodes(self, edge):
        nodes = []
        for _ in range(self.nodecount):
            nodes.append(np.array([
                    random.random() * self.coordinate_range,         
                    random.random() * self.coordinate_range
                ]))
        return nodes

    def _generate_distances(self):
        distances = np.zeros((self.nodecount, self.nodecount))
        for x, n1 in enumerate(self.nodes):
            for y, n2 in enumerate(self.nodes):
                distances[x, y] = self._distance(n1, n2)
        return distances

    @staticmethod
    def _distance(p1, p2):
        # Compute euclidian distance between the two given inputs.
        p1, p2 = np.array(p1), np.array(p2)
        return np.linalg.norm(p1-p2)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"TSP with {self.nodecount} nodes."

def tsp_mutate(probability, amount):
    @mutation_operator
    def result (solution):
        mutated = solution
        for i in range(amount):
            if random.random() < probability:
                i = random.randint(0, len(solution)-1)
                j = random.randint(0, len(solution)-1)
                solution[[i, j]] = solution[[j, i]]
        return mutated
    return result

def get_evolution(tsp, pop_size, output_fp, mutation_probability, mutation_number):
    """ Helper function that creates a TSP-evolution based on some given settings. """
    headers = ['fittest', 'mean', 'median']
    formatter = lambda evolution: [round(evolution.get_fittest_individual()[1], DIGITS), round(evolution.get_mean_fitness(), DIGITS), round(evolution.get_median_fitness(), DIGITS)]

    evolution = Evolution(pop_size, tsp.random_solution, tsp.solution_cost, cutoff_selection, [tsp_mutate(mutation_probability, mutation_number)], proportional=False, writer=CSVWriter(output_fp, formatter, headers))
    return evolution

class TSPAnimation:
    def __init__(self, tsp, evolution):
        self.tsp = tsp
        self.evolution = evolution
        self.lines = None
        self.text = None

    def update(self, evolution, ax, i):
        if self.lines is not None:
            for line in self.lines:
                line.remove()
        if self.text is not None:
            self.text.remove()
        fittest, fitness = evolution.get_fittest_individual()
        self.text = ax.text(0, 0, f"generation: {evolution.generation}; fitness: {fitness}")
        print(f"{evolution.generation} : {fitness}")
        # The first element of the list has to be appended at the end again, so that it entails the full hamilton cycle.
        fittest_cycle = np.append(fittest, [fittest[0]], axis=0)
        fittest_cycle = np.array([self.tsp.nodes[index] for index in fittest_cycle]) # Convert indices to actual nodes. 
        X, Y = fittest_cycle.T
        self.lines = ax.plot(X, Y, c=COLOR)
        evolution.step()
        

    def setup(self, evolution, ax):
        ax.scatter(*list(zip(*self.tsp.nodes)))


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    tsp = TSP(int(arguments['<nodecount>']))
    evolution = get_evolution(tsp, int(arguments['<popsize>']), arguments['<outputfile>'], float(arguments['<mprob>'])/100, int(arguments['<mnum>']))
    animation = TSPAnimation(tsp, evolution)
    view = View([evolution], (1, 1), animation.update, animation.setup, blit=False)
    view.run()
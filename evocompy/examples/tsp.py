"""
Usage:
    tsp.py <nodecount> <popsize> <outputfile>
"""
import random

import docopt
import numpy as np
import matplotlib.pyplot as plt

from ..evolution import Evolution, mutation_operator, cutoff_selection
from ..view import View
from ..io import CSVWriter


DIGITS = 2

class TSP: 
    """ Implementation of the traveling salesperson problem. """
    def __init__(self, nodecount, coordinate_range=1):
        self.nodecount = nodecount
        self.coordinate_range = coordinate_range
        self.nodes = self._generate_nodes(nodecount)
        self.distances = self._generate_distances()
        

    def random_solution(self):
        """ Returns a uniformly randomized solution for the tsp. """
        nodes = self.nodes 
        np.random.shuffle(nodes)
        return nodes

    def get_distance(self, edge):
        """ Returns the cost of a potential edge of the graph. Utilizes the underlying representation of the cost matrix as a dictionary. """
        return self.distances[edge]

    def solution_cost(self, solution):
        cost = 0.0
        for i in range(len(solution)):
            cost += self.get_distance(frozenset((tuple(solution[i]), tuple(solution[i%len(solution)]))))
        return cost

    def _generate_nodes(self, edge):
        nodes = []
        for _ in range(self.nodecount):
            nodes.append((
                    random.random() * self.coordinate_range,         
                    random.random() * self.coordinate_range
                ))
        return nodes

    def _generate_distances(self):
        distances = dict()
        for p1 in self.nodes:
            for p2 in self.nodes:
                s = frozenset((p1, p2))
                if s not in distances:
                    distances[s] = self._distance(p1, p2) 
        return distances

    @staticmethod
    def _distance(p1, p2):
        p1, p2 = np.array(p1), np.array(p2)
        return np.linalg.norm(p1-p2)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"TSP with {self.nodecount} nodes."

@mutation_operator
def tsp_mutate(solution, probability, amount):
    mutated = solution
    for i in range(amount):
        if random.random() < probability:
            i = random.randint(0, len(solution)-1)
            j = random.randint(0, len(solution)-1)
            solution[[i, j]] = solution[[j, i]]
    return mutated

def get_evolution(tsp, pop_size, output_fp):
    headers = ['fittest', 'mean', 'median']
    formatter = lambda evolution: [round(evolution.get_fittest_individual()[1], DIGITS), round(evolution.get_mean_fitness(), DIGITS), round(evolution.get_median_fitness(), DIGITS)]

    evolution = Evolution(pop_size, tsp.random_solution, tsp.solution_cost, cutoff_selection, [tsp_mutate], proportional=False, writer=CSVWriter(output_fp, formatter, headers))
    return evolution

class TSPAnimation:
    def __init__(self, tsp, evolution):
        self.tsp = tsp
        self.evolution = evolution
        self.lines = None

    def update(self, evolution, ax, i):
        if self.lines is not None:
            self.lines.remove()
        
        print(evolution.generation)
        evolution.step()

    def setup(self, evolution, ax):
        ax.scatter(*list(zip(*self.tsp.nodes)))

    def teardown(self, evolution):
        ...


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    tsp = TSP(int(arguments['<nodecount>']))
    evolution = get_evolution(tsp, int(arguments['<popsize>']), arguments['<outputfile>'])
    animation = TSPAnimation(tsp, evolution)
    view = View([evolution], (1, 1), animation.update, animation.setup)
    plt.show()
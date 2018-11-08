from .evolution import Evolution
from .io import CSVWriter

def condition_generation(n):
    """ Returns a condition function that can be passed to a Benchmark and
        stops the benchmark after n generations. 
    """
    return lambda evolution: evolution.generation < n-1

def condition_best_fitness(v):
    """ Returns a condition function that can be passed to a Benchmark and 
        stops the benchmark when the best fitness is greater than or equal to v. 
    """
    return lambda evolution: evolution.get_fittest_individual()[1] < v

class Benchmark:
    """ The Benchmark class is a test runner that allows the user to run a set of evolutions
        without an interface. The condition argument is a function that takes the evolution
        as an argument and returns a boolean that determines if the program should continue
        running.
    """
    def __init__(self, evolutions, condition):
        self.evolutions = evolutions
        self.condition = condition

    def run(self):
        """ Runs the benchmark. """
        for evolution in self.evolutions:
            while self.condition(evolution):
                evolution.step()

class AverageEvolution:
    def __init__(self, count, *args, **kwargs):
        self.evolutions = []
        self.count = count
        self.writer = AverageCSVWriter()
        for _ in range(self.count):
            self.evolutions.append(Evolution(*args, writer=self.writer, **kwargs))

    def step(self): 
        for evolution in self.evolutions:
            evolution.step()



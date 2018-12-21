# Evocompy

Small library that enables the user to quickly construct evolutionary algorithms.
A german version of this readme can be found [here](https://github.com/erikps/evocompy/wiki/%5BDE%5D-Dokumentation)

## Installation

This library can be easily installed through the pip command line tool:
```sh
pip install git+https://github.com/erikps/evocompy.git
```

## Usage

The Evolution class is the centerpiece of this library. You can create an instance of this class to construct an evolutionary algorithm. To initialize it, there are some required arguments:
* The (initial) population size.
* A random function that returns a randomized genotype / solution
* A fitness function that evaluates a solution. Note that a genotype-phenotype-mapping has to be implemented manually inside of this function as it takes a genotype as input.
* The selection scheme to be applied. There are some already provied, e.g. cutoff and roulette-wheel selection. The selection method is responsible for selecting a subset of the population, and based thereof create a new population (the next generation).
* Lastly, an iterable of genetic operators is required. A genetic operator takes in a population and somehow mutates or mixes the genepool. Generally mutation and crossover of some form are utilized. Note that mutation probability is not handled by this implementation.

The Evolution class assumes a generational model, a steady-state approach is not supported.

You can then run the newly constructed algorithm using the `step()` method. This will run the algorithm one time, creating a new generation. 
  At any time, queries about the current fitness landscape can be made, using the `get_mean_fitness()` and `get_median_fitness()` functions can be made. The fittest individual can be accessed by `get_fittest_individual()` which returns a tuple including the individual and its respective fitness. 

## Dependencies
* Numpy
* Docopt for the command line interface
* Matplotlib for displaying results

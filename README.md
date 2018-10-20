# evocompy
Lightweight evolutionary computation algorithm.

## Usage

### Basic

The Evolution class is the centerpiece of this library. You can create an instance of this class to construct an evolutionary algorithm. For this general evolution settings, a random function, a fitness function and a mutation function are needed. The random function has to return a random genotype.  
```python

evolution = Evolution (settings, initital_population, fitness_function, muatation_function) 
```

You can then run the newly constructed algorithm using the `step()` method. This will run the algorithm one time, creating a new generation. 
  At any time, queries about the current fitness landscape can be made, using the `get_mean_fitness()` and `get_median_fitness()` functions can be made. The fittest individual can be accessed by `get_fittest_individual()` which returns a tuple including the individual and its respective fitness. 

## Used Libraries
* Numpy
* Docopt for the command line interface
* Matplotlib for displaying results

## Todo

* Implement smater ways to perform selection to allow for more complex analysis.
* Implement support for schemata (á la Goldberg) to allow for more complex analysis.


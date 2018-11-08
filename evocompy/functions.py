"""

Usage:
    cli.py -h | --help
    cli.py <function-name> <min> <max> <step> [-f | --from-file] <filepath>
    cli.py <function-name> <min> <max> <step> [-f | --from-file] <filepath> [-b | --benchmark] <generations> <namepattern>
    cli.py <function-name> <min> <max> <step> [-f | --from-file] <filepath> [-b | --benchmark] <generations> <namepattern> [--mean] <amount>
    cli.py <function-name> <min> <max> <step> [-f | --from-file] <filepath> [-i | --interval] <interval>  

Options:
    -h --help        Show this screen.
    -f --from-file   Create a view from a settings file.

"""

import math
import random
import sys

from docopt import docopt

sys.path.append('..')

from .evolution2d import Evolution2D, settings2d_from_file, function_dict
from .view import View2D
from .io import CSVWriter, HistoryWriter
from .benchmark import Benchmark, condition_generation

DIGITS = 2

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0')
    
    function = lambda x: 0
    settings = []
    interval = 50

    if arguments['<function-name>'] and arguments['<function-name>'] in function_dict:
        function = function_dict[arguments['<function-name>']]
    
    if arguments['--from-file'] or arguments['-f']:
        # TODO: This try/except block is boilerplate code.
        try:
            settings = settings2d_from_file(arguments['<filepath>']) 
        except Exception as E:
            print ('Invalid input file!')
            exit(1)

    if arguments['--interval'] or arguments['-i']:
        interval = float(arguments['<interval>'])

    value_range = (float(arguments['<min>']), float(arguments['<max>']))
    step = float(arguments['<step>'])
    
    size = int(math.ceil(math.sqrt(len(settings))))
    layout = (size, size)
<<<<<<< HEAD
    view = View2D(function, layout, settings, value_range, step, interval=interval)
    view.run()
=======

    headers = ['fittest', 'mean', 'median']
    formatter = lambda evolution: [round(evolution.get_fittest_individual()[1], DIGITS), round(evolution.get_mean_fitness(), DIGITS), round(evolution.get_median_fitness(), DIGITS)]

    if arguments['-b'] or arguments['--benchmark']:
        generations = 0
        try:
            generations = int(arguments['<generations>'])
        except Exception as E:
            print('Please enter an integer as the generation count!')
            exit(1)

        evolutions = []
        for i, setting in enumerate(settings):
            evolutions.append(Evolution2D(function, setting, value_range, step, writer=CSVWriter(f"{arguments['<namepattern>']}{i}.csv", formatter, headers)))
        benchmark = Benchmark(evolutions, condition_generation(generations))
        benchmark.run()

    else: 
        view = View2D(function, layout, settings, value_range, step, interval=interval, writer=CSVWriter('functions.csv', formatter, headers))
        view.run()
>>>>>>> f8acefb7c4e41d924ba72881a681c41ed6627908

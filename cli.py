"""

Usage:
    cli.py -h | --help
    cli.py <function-name> <min> <max> <step> [-f | --from-file] <filepath>
    cli.py <function-name> <min> <max> <step> [-f | --from-file] <filepath> [-i | --interval] <interval> [-d | --distribution] <distribution> 

Options:
    -h --help        Show this screen.
    -f --from-file   Create a view from a settings file.

"""

import math
import random
import sys

from docopt import docopt

sys.path.append('..')

from evolution2d import Evolution2D, settings2d_from_file, distribution_dict, function_dict
from view import View2D


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

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0')
    
    function = lambda x: 0
    settings = []
    interval = 50

    if arguments['<function-name>'] and arguments['<function-name>'] in function_dict:
        function = function_dict[arguments['<function-name>']]
    
    if arguments['--from-file'] or arguments['-f']:
        settings = settings2d_from_file(arguments['<filepath>']) 

    if arguments['--interval'] or arguments['-i']:
        interval = float(arguments['<interval>'])

    if arguments['--distribution'] or arguments

    value_range = (float(arguments['<min>']), float(arguments['<max>']))
    step = float(arguments['<step>'])
    
    size = int(math.ceil(math.sqrt(len(settings))))
    layout = (size, size)
    view = View2D(function, layout, settings, value_range, step, interval=interval)
    view.run()

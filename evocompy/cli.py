"""

Usage:
    cli.py -h | --help
    cli.py <function-name> <min> <max> <step> [-f | --from-file] <filepath>
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

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0')
    
    function = lambda x: 0
    settings = []
    interval = 50

    if arguments['<function-name>'] and arguments['<function-name>'] in function_dict:
        function = function_dict[arguments['<function-name>']]
    
    if arguments['--from-file'] or arguments['-f']:
        try:
            settings = settings2d_from_file(arguments['<filepath>']) 
        except:
            print ('Invalid input file!')
            exit(1)

    if arguments['--interval'] or arguments['-i']:
        interval = float(arguments['<interval>'])

    value_range = (float(arguments['<min>']), float(arguments['<max>']))
    step = float(arguments['<step>'])
    
    size = int(math.ceil(math.sqrt(len(settings))))
    layout = (size, size)
    print(f"{function}, {layout}, {settings}")
    view = View2D(function, layout, settings, value_range, step, interval=interval)
    view.run()

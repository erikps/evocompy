import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import ticker, cm, style

import numpy as np

from evolution2d import Evolution2D

class View:
    """ Evolutionary algorithm related plotting, using matplotlib. 
        The animate constructor is a higher order function that takes 
    """
    
    def __init__(self, evolutions, layout, animate, setup, interval=50, teardown=None, frames=None):
        if not layout[0]*layout[1] >= len(evolutions):
            raise ValueError("Not enough space in specified layout. ")               
        
        self.evolutions = evolutions
        self.animate = animate        
        self.rows, self.columns = layout
        self.teardown = teardown
        self.fig, self.axes = plt.subplots(self.rows, self.columns)
        self.axes = np.array([self.axes]).flatten()
        for i, evolution in enumerate(self.evolutions):
            setup(evolution, self.axes[i])
        self.animation = animation.FuncAnimation(self.fig, self._animate, interval=interval, blit=True, frames=frames)

    def run(self):
        plt.show()

    def export_to_mp4(self, filepath):
        self.animation.save(filepath)

    def _animate(self, i):
        points = []
        for n, evolution in enumerate(self.evolutions):
            points.append(self.animate(evolution, self.axes[n], i))
        if self.teardown is not None:
            for n, ax in enumerate(self.axes):
                self.teardown(ax, n)
        return points

class View2D(View):
    """ View for evolutions of 2 dimensional functions.
    """
    def __init__(self, function, layout, settings, value_range, value_step, cmap=cm.Blues, interval=50):
        evolutions = []
        for setting in settings:
            evolution = Evolution2D(function, setting, value_range, value_step)
            evolutions.append(evolution)
        self.cmap = cmap
        self._to_remove = []
        super().__init__(evolutions, layout, self._update, self._setup, interval=interval)

    def _setup(self, evolution, ax): 
        mi, ma = evolution.value_range
        ax.set_xlim(mi, ma)
        ax.set_ylim(mi, ma)
        X, Y, Z = evolution.create_values()
        X, Y = np.meshgrid(X, Y)
        ax.contourf(Y, X, Z, locator=ticker.LinearLocator(), cmap=self.cmap)

    def _update(self, evolution, ax, i):
        transposed = evolution.evolution.current_population.transpose()
        points = (ax.scatter(transposed[0], transposed[1], marker='.', c='orange')) 
        evolution.evolution.step()
        return points

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import ticker, cm, style

import numpy as np

from .evolution2d import Evolution2D

class View:
    """ Evolutionary algorithm related plotting, using matplotlib. 
        The animate constructor is a higher order function that takes 
    """
    
    def __init__(self, evolutions, layout, animate, setup, interval=50, teardown=None, frames=None, blit=True, pause_generations=[1]):
        if not layout[0]*layout[1] >= len(evolutions):
            raise ValueError("Not enough space in specified layout. ")               
        
        self.evolutions = evolutions
        self.animate = animate        
        self.rows, self.columns = layout
        self.teardown = teardown
        self.pause_generations = pause_generations
        self.fig, self.axes = plt.subplots(self.rows, self.columns)
        self.fig.canvas.mpl_connect('close_event', self._finalize)
        self.axes = np.array([self.axes]).flatten()
        self.pause = False
        for i, evolution in enumerate(self.evolutions):
            setup(evolution, self.axes[i], self.fig)
        self.animation = animation.FuncAnimation(self.fig, self._animate, interval=interval, blit=blit, frames=frames)
        self.fig.canvas.mpl_connect('button_press_event', self._onClick)

    def run(self):
        """ Runs the view on the activated matplotlib frontend. """
        plt.show()

    def export(self, filepath):
        """ Saves the View2D as an animation to the specified path. """  
        self.animation.save(filepath)

    def _animate(self, i):
        points = []
        for n, evolution in enumerate(self.evolutions):
            if not self.pause:
                points.append(self.animate(evolution, self.axes[n], self.fig, i))
            if evolution.generation in self.pause_generations:
                self.pause = True
        if self.teardown is not None:
            for n, ax in enumerate(self.axes):
                self.teardown(ax, n)
        return points

    def _finalize(self, evt):
        for evolution in self.evolutions:
            evolution.finalize_writer()
        
    def _onClick(self, event):
        self.pause ^= True

class View2D(View):
    """ View for evolutions of 2 dimensional functions.
    """
    def __init__(self, function, layout, settings, value_range, value_step, cmap=cm.Blues, interval=50, frames=None, writer=None):
        evolutions = []
        for setting in settings:
            evolution = Evolution2D(function, setting, value_range, value_step, writer=writer)
            evolutions.append(evolution)
        self.cmap = cmap
        self._to_remove = []
        self.points = None
        super().__init__(evolutions, layout, self._update, self._setup, interval=interval, frames=frames)

    def _setup(self, evolution, ax, fig): 
        mi, ma = evolution.value_range
        ax.set_xlim(mi, ma)
        ax.set_ylim(mi, ma)
        X, Y, Z = evolution.create_values()
        X, Y = np.meshgrid(X, Y)
        ax.contourf(Y, X, Z, locator=ticker.LinearLocator(), cmap=self.cmap)
        self._animation(evolution, ax)

    def _update(self, evolution, ax, fig, i):
        self._animation(evolution, ax)
        evolution.step()    
        return self.points

    def _animation(self, evolution, ax):
        transposed = evolution.current_population.transpose()
        self.points = ax.scatter(transposed[0], transposed[1], marker='.', c='orange') 


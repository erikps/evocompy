import csv
import json

import numpy as np

class _NumpyEncoder(json.JSONEncoder):
    # Small helper class for encoding numpy arrays into JSON.
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class History:
    """ In a History object, information about past generations of an Evolution can be stored. """
    def __init__(self, generations, filepath=None):
        self.generations = generations
        self.filepath = filepath

    def add(self, generation):
        """ Adds a generation to the history. """
        self.generations.append(generation)

    def write_json(self):
        """ Writes history into a json file. """
        with open(self.filepath, mode='w', encoding='utf-8') as f:
            json.dump(self.generations, f, cls=_NumpyEncoder)

class CSVWriter:
    """ Implements a writer class that can write information about an Evolution into a csv file. """
    def __init__(self, filepath, format_function, headers, delimiter=','):
        self.filepath = filepath
        self.format_function = format_function
        self.headers = headers
        self.delimiter = delimiter
        with open(self.filepath, mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(headers)

    def step(self, evolution):
        """ Appends the next line to the csv. """
        with open(self.filepath, mode='a', newline='') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(self.format_function(evolution))
            

    def finalize(self):
        """ Only implemented so that no error is thrown. """
        ...

class HistoryWriter:
    """ Writer that fills a History object with data. """"
    def __init__(self, filepath=None):
        self.history = History([], filepath=filepath)
    
    def step(self, evolution):
        """ Appends the next generation to the history. """
        self.history.add(evolution.current_generation)

    def finalize(self):
        """ If the history has a filepath, the data is serialized into it as JSON. """
        if self.history.filepath is not None:
            self.history.write_json()

import csv
import json

import numpy as np

class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class History:
    def __init__(self, generations, filepath=None):
        self.generations = generations
        self.filepath = filepath

    def add(self, generation):
        self.generations.append(generation)

    def write_json(self):
        with open(self.filepath, mode='w', encoding='utf-8') as f:
            json.dump(self.generations, f, cls=_NumpyEncoder)

class CSVWriter:
    def __init__(self, filepath, format_function, headers, delimiter=','):
        self.filepath = filepath
        self.format_function = format_function
        self.headers = headers
        self.delimiter = delimiter
        with open(self.filepath, mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(headers)

    def step(self, evolution):
        with open(self.filepath, mode='a', newline='') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(self.format_function(evolution))
            

    def finalize(self):
        ...

class HistoryWriter:
    def __init__(self, filepath=None):
        self.history = History([], filepath=filepath)
    
    def step(self, evolution):
        self.history.add(evolution.current_generation)

    def finalize(self):
        if self.history.filepath is not None:
            self.history.write_json()
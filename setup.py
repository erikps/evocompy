#!/usr/bin/env python
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'evocompy',
    version = '0.1.0',
    author = 'erikps',
    author_email = 'erikps.github@gmail.com',
    description = 'Lightweight evolutionary computation framework',
    long_description = long_description,
    url = 'https://github.com/erikps/evocompy',
    packages = setuptools.find_packages(exclude=['evocompy/functions.py']),
    scripts=['evocompy/functions.py', 'evocompy/examples/tsp.py'],
    classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI approved :: MIT License',
            'Operating System :: OS Independent',
        ],
    )

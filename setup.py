#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='flaskerize',
      version='0.1.3',
      description='Bundle and serve static web applications such as Angular or React '
                  'with Flask APIs through a single, Flask app',
      author='AJ Pryor',
      author_email='apryor6@gmail.com',
      url='http://alanpryorjr.com/',
      packages=find_packages(),
      scripts=['bin/flaskerize', 'bin/fz']
      )

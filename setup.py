#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="flaskerize",
    version="0.3.4",
    description="Flask CLI build/dev tool for bundling static sites into Flask apps and templated code generation",
    author="AJ Pryor",
    author_email="apryor6@gmail.com",
    url="http://alanpryorjr.com/",
    packages=find_packages(),
    install_requires=["Flask>=1.1.1", "termcolor>=1.1.0"],
    scripts=["bin/fz"],
)

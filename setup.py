#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="flaskerize",
    version="0.1.10",
    description="Flask CLI build/dev tool for bundling static sites into Flask apps and templated code generation",
    author="AJ Pryor",
    author_email="apryor6@gmail.com",
    url="http://alanpryorjr.com/",
    packages=find_packages(),
    scripts=["bin/flaskerize", "bin/fz"],
)

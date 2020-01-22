#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="flaskerize",
    version="0.14.0",
    description="Python CLI build/dev tool for templated code generation and project modification. Think Angular schematics for Python.",
    author="AJ Pryor",
    author_email="apryor6@gmail.com",
    url="http://alanpryorjr.com/",
    packages=find_packages(),
    install_requires=["Flask>=1.1.1", "termcolor>=1.1.0", "fs>=2.4.10"],
    include_package_data=True,
    scripts=["bin/fz"],
)

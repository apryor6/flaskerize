flaskerize
==========

**flaskerize** is a code generation and project modification command line interface (CLI) written in Python and created for Python.
It is heavily influenced by concepts and design patterns of the Angular CLI available in the popular JavaScript framework Angular.
In addition to vanilla template generation, flaskerize supports hooks for custom run methods and registration of user-provided template functions.
It was built with extensibility in mind so that you can create and distribute your own library of :term:`schematics`  for just about anything.

Use **flaskerize** for tasks including:

- Generating resources such as Dockerfiles, new **flaskerize** :term:`schematics` , blueprints, yaml configs, SQLAlchemy entities, or even entire applications, all with functioning tests
- Upgrading between breaking versions of projects that provide flaskerize upgrade :term:`schematics`  with one command
- Bundling and serving static web applications such as Angular, React, Gatsby, Jekyll, etc within a new or existing Flask app.
- Registering Flask resources as new routes within an existing application
- Creating new :term:`schematics`  for your own library or organization

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  quick-start/index
  contributing
  glossary


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

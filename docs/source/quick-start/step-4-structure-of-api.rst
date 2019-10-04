Step 4: The Structure of your Flask API
=======================================

In the previous step we created a Flask API using the **flaskerize** command ``fz generate flask-api my_app``.
This generated a number of file and folders, so let's take a look at what you have.

The set of files and folders that were created are illustrated below:

.. code-block:: text

  .
  ├── README.md
  ├── app
  │   ├── __init__.py
  │   ├── config.py
  │   ├── routes.py
  │   ├── test
  │   │   ├── __init__.py
  │   │   └── fixtures.py
  │   └── widget
  │       ├── __init__.py
  │       ├── controller.py
  │       ├── interface.py
  │       ├── model.py
  │       ├── schema.py
  │       └── service.py
  ├── commands
  │   ├── __init__.py
  │   └── seed_command.py
  ├── manage.py
  ├── requirements.txt
  └── wsgi.py

Let's take a closer look at what these files do.

+---------------------+-----------------------------------------------+
| name                | description                                   |
+=====================+===============================================+
|  README.md          | | A markdown file containing instructions for |
|                     | | setting up and running your Flask API       |
+---------------------+-----------------------------------------------+
|  app                | This folder contains your Flask API code      |
+---------------------+-----------------------------------------------+
| commands            | | This folder contains the code that seeds the|
|                     | | database with data                          |
+---------------------+-----------------------------------------------+
|  manage.py          | Exposes the database setup commands           |
+---------------------+-----------------------------------------------+
|  requirements.txt   | | Contains the list of dependencies. Used for |
|                     | | ``pip install -r requirements.txt``         |
+---------------------+-----------------------------------------------+
|  wsgi.py            | | Contains code that creates an instance of   |
|                     | | your Flask API                              |
+---------------------+-----------------------------------------------+

Entities
--------

Within the ``app` folder you can see there's folder called ``widget``.
This folder contains code related to the ``widget`` entity.

Each entity folder contains:

- ``controller.py`` - contains
- ``interface.py`` - contains
- ``model.py`` - contains
- ``schema.py`` - contains
- ``service.py`` - contains

You can read more about this structure in the following blog post:

http://alanpryorjr.com/2019-05-20-flask-api-example/

In the next part of this tutorial we will add an additional entity to our api.

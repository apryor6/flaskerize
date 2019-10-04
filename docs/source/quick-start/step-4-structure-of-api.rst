Step 4: The Structure of your Flask API
=======================================

In the previous step we created a Flask API using the **flaskerize** command ``fz generate flask-api my_app``.
This generated a number of file and folders, so let's take a look at what you have.


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

TODO: add details here

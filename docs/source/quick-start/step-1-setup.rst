Step 1: Setting up Flaskerize
=============================

We're going to start from nothing, and over the course of this quickstart we'll end up with a simple API.

First, let's create a folder for our Flask API to live in.

.. code:: bash

    mkdir flaskerize-example
    cd flaskertize-example


Now, let's set up a virtual environment for our API project, activate it,
and then upgrade ``pip`` within that environment.

.. code:: bash

    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip

.. note:: The last command, ``pip install --upgrade pip``, ensures that we have the latest version of ``pip`` installed.

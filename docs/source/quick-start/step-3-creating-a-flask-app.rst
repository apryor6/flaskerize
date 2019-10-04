Step 3: Creating the Flask API
==============================

You're we're now ready to create our Flask API, and we're going to use **flaskerize** to do most of this for us.

**flaskerize** has a number of :term:`generators` that generate code and configuration for us.
These :term:`generators` use :term:`schematics` to define exactly what code should be built.
There are a number of :term:`schematics` build into  **flaskerize**.

We're going to start by using the ``flask-api`` generator to create a simple Flask API.

From the root of your project folder, run the following command:

.. code-block:: bash

  fz generate flask-api my_app

You'll see output similar to the following:

.. code-block:: bash

  $ fz generate flask-api my_app
  Flaskerizing...

  Flaskerize job summary:

          Schematic generation successful!
          Full schematic path: flaskerize/schematics/flask-api



          13 directories created
          40 file(s) created
          0 file(s) deleted
          0 file(s) modified
          0 file(s) unchanged

  CREATED: flaskerize-example/.pytest_cache
  CREATED: flaskerize-example/.pytest_cache/v
  CREATED: flaskerize-example/.pytest_cache/v/cache
  CREATED: flaskerize-example/my_app
  CREATED: flaskerize-example/my_app/__pycache__
  CREATED: flaskerize-example/my_app/app
  CREATED: flaskerize-example/my_app/app/__pycache__
  CREATED: flaskerize-example/my_app/app/test
  CREATED: flaskerize-example/my_app/app/test/__pycache__
  CREATED: flaskerize-example/my_app/app/widget
  CREATED: flaskerize-example/my_app/app/widget/__pycache__
  CREATED: flaskerize-example/my_app/commands
  CREATED: flaskerize-example/my_app/commands/__pycache__
  CREATED: .gitignore
  CREATED: .pytest_cache/.gitignore
  CREATED: .pytest_cache/CACHEDIR.TAG
  CREATED: .pytest_cache/README.md
  CREATED: .pytest_cache/v/cache/lastfailed
  CREATED: .pytest_cache/v/cache/nodeids
  CREATED: .pytest_cache/v/cache/stepwise
  CREATED: my_app/README.md
  CREATED: my_app/__pycache__/manage.cpython-37.pyc
  CREATED: my_app/__pycache__/wsgi.cpython-37.pyc
  CREATED: my_app/app/__init__.py
  CREATED: my_app/app/__pycache__/__init__.cpython-37.pyc
  CREATED: my_app/app/__pycache__/config.cpython-37.pyc
  CREATED: my_app/app/__pycache__/routes.cpython-37.pyc
  CREATED: my_app/app/app-test.db
  CREATED: my_app/app/config.py
  CREATED: my_app/app/routes.py
  CREATED: my_app/app/test/__init__.py
  CREATED: my_app/app/test/__pycache__/__init__.cpython-37.pyc
  CREATED: my_app/app/test/__pycache__/fixtures.cpython-37.pyc
  CREATED: my_app/app/test/fixtures.py
  CREATED: my_app/app/widget/__init__.py
  CREATED: my_app/app/widget/__pycache__/__init__.cpython-37.pyc
  CREATED: my_app/app/widget/__pycache__/controller.cpython-37.pyc
  CREATED: my_app/app/widget/__pycache__/interface.cpython-37.pyc
  CREATED: my_app/app/widget/__pycache__/model.cpython-37.pyc
  CREATED: my_app/app/widget/__pycache__/schema.cpython-37.pyc
  CREATED: my_app/app/widget/__pycache__/service.cpython-37.pyc
  CREATED: my_app/app/widget/controller.py
  CREATED: my_app/app/widget/interface.py
  CREATED: my_app/app/widget/model.py
  CREATED: my_app/app/widget/schema.py
  CREATED: my_app/app/widget/service.py
  CREATED: my_app/commands/__init__.py
  CREATED: my_app/commands/__pycache__/__init__.cpython-37.pyc
  CREATED: my_app/commands/__pycache__/seed_command.cpython-37.pyc
  CREATED: my_app/commands/seed_command.py
  CREATED: my_app/manage.py
  CREATED: my_app/requirements.txt
  CREATED: my_app/wsgi.py

Confirm your API is working
^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, let's check that your API is working, then after that we'll dig into what happened.

You can use the Flask command line interface to confirm that your Flask API is working by first using the ``flask routes`` command.
This will print out all of the routes supported by your Flask API:

.. code-block:: bash

  $ flask routes
  Endpoint                   Methods           Rule
  -------------------------  ----------------  --------------------------
  Widget_widget_id_resource  DELETE, GET, PUT  /api/widget/<int:widgetId>
  Widget_widget_resource     GET, POST         /api/widget/
  doc                        GET               /
  health                     GET               /health
  restplus_doc.static        GET               /swaggerui/<path:filename>
  root                       GET               /
  specs                      GET               /swagger.json
  static                     GET               /static/<path:filename>

As you can see, a number of routes have been generated.

Now, you can run your Flask API using ``flask run`` or by running ``python wsgi.py``:

.. code-block:: bash

  $ python wsgi.py
  * Serving Flask app "app" (lazy loading)
  * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
  * Debug mode: on
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  * Restarting with stat
  * Debugger is active!
  * Debugger PIN: 304-898-518


While the Flask app is running, open http://127.0.0.1:5000/health within your favourite browser,
and you should be greated with the Swagger documentation for your API.

.. image:: images/health-endpoint.png

In the next section we'll dig into what happened when you ran ``fz generate flask-api my_app`` and the structure of your Flask API.

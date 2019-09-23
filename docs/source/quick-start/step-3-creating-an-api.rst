Step 3: Creating an API
=======================

You're now ready to create your Flask API. 
To make this simple, **flaskerize** has a number of :term:`generators` that will build code or you.
These :term:`generators` used :term:`schematics` to define the code that's built.

We're going to start by using the ``app`` generator to create the basics of our API application.

From the root of your project folder, run the following command:

.. code-block:: bash

  fz generate app wsgi

You'll see output similar to the following:

.. code-block:: bash

  $ fz generate app wsgi
  Flaskerizing...

  Flaskerize job summary:

          Schematic generation successful!
          Full schematic path: flaskerize/schematics/app

          0 directories created
          1 file(s) created
          0 file(s) deleted
          0 file(s) modified
          0 file(s) unchanged

  CREATED: wsgi.py

As you can see, this has generated a file called ``wsgi.py``. This file should contain the following:

.. code-block:: python

  import os
  from flask import Flask


  def create_app():
      app = Flask(__name__)

      @app.route("/")
      @app.route("/health")
      def serve():
          return "wsgi online!"

      return app


  if __name__ == "__main__":
      app = create_app()
      app.run()


This code is a very basic, but functioning, Flask app. 
You can use the flask command line interface to confirm this by running ``flask routes``,
which will print out the routes that Flask is aware of...

.. code-block:: bash

  $ flask routes
  Endpoint  Methods  Rule
  --------  -------  -----------------------
  serve     GET      /health
  serve     GET      /
  static    GET      /static/<path:filename>

From this output you can see there are three routes. Let's run the Flask app, and test the ``/health`` route.
Use the flask command ``flask run`` to launch your Flask app:

.. code-block:: bash

    $ flask run
  * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
  * Debug mode: off
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


While the Flask app is running, open http://127.0.0.1:5000/health within your favourite browser,
and you should see the message "wsgi online!" displayed:

.. image:: images/health-endpoint.png

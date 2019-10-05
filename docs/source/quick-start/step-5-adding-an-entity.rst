Step 5: Adding Entities to an API
=================================

Over the previous steps we've built our Flask API. It already has a ``widget`` :term:`entity`,
but now we're going to add another :term:`entity`.

We are going to add a ``cake`` :term:`entity`.

To do this we're going to use another of **flaskerize's** :term:`schematics`; the ``entity`` schematic.

From within the ``my_app`` folder we'll use the following command  to generate our ``cake`` entity:

.. code-block:: bash

  fz generate entity app/cake

This command will generate an entity, called cake, within the ``app`` folder.

.. code-block:: bash

  $ fz generate entity app/cake
  Flaskerizing...

  Flaskerize job summary:

          Schematic generation successful!
          Full schematic path: flaskerize/schematics/entity



          1 directories created
          11 file(s) created
          0 file(s) deleted
          0 file(s) modified
          0 file(s) unchanged

  CREATED: flaskerize-example/my_app/app/cake
  CREATED: app/cake/__init__.py
  CREATED: app/cake/controller.py
  CREATED: app/cake/controller_test.py
  CREATED: app/cake/interface.py
  CREATED: app/cake/interface_test.py
  CREATED: app/cake/model.py
  CREATED: app/cake/model_test.py
  CREATED: app/cake/schema.py
  CREATED: app/cake/schema_test.py
  CREATED: app/cake/service.py
  CREATED: app/cake/service_test.py


So, what just happened?

- A folder named ``cake`` was created under the ``app`` folder. Everything related to the ``cake`` entity lives within this folder.
- A set of python files relating to the ``cake`` entity were created
- A set of tests, relating to the ``cake`` entity were also created

Wiring Up the New Cake Entity
-----------------------------

If you run the ``flask routes`` command, or run ``python wsgi.py``, you won't see any additional routes
and you won't see your ``cake`` entity appear within the Swagger docs.

This is because there's some manual wire-up that you now need to do.

First, we need to edit the code within ``my_app/app/routes.py``. Open this file in a text editor and add
the following 2 lines of code (each addition has a comment starting with ``ADD THE FOLLOWING LINE`` above it):

.. code-block:: python

  def register_routes(api, app, root="api"):
      from app.widget import register_routes as attach_widget

      # ADD THE FOLLOWING LINE to import the register_routes function
      from app.cake import register_routes as attach_cake

      # Add routes
      attach_widget(api, app)

      # ADD THE FOLLOWING LINE to register the routes for the cake entity
      attach_cake(api)

Now, when you run ``flask route`` you'll see the additional routes for your ``cake`` entity.
Additionally, you can now see the ``cake`` entity appear in the Swagger docs UI:

.. image:: images/cake-entity-added.png

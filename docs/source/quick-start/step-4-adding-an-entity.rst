Step 4: Adding Entities to an API
=================================

Now that we have a **very** basic Flask app, we're going to add an :term:`entity` to it.

We'll use the command ``fz generate entity cake`` which will use the ``entity`` schematic to generate code
for an entity called `cake`.

.. code-block:: bash

  $ fz generate entity cake
  Flaskerizing...

  Flaskerize job summary:

          Schematic generation successful!
          Full schematic path: flaskerize/schematics/entity



          1 directories created
          11 file(s) created
          0 file(s) deleted
          0 file(s) modified
          0 file(s) unchanged

  CREATED: flaskerize-example/cake
  CREATED: cake/__init__.py
  CREATED: cake/controller.py
  CREATED: cake/controller_test.py
  CREATED: cake/interface.py
  CREATED: cake/interface_test.py
  CREATED: cake/model.py
  CREATED: cake/model_test.py
  CREATED: cake/schema.py
  CREATED: cake/schema_test.py
  CREATED: cake/service.py
  CREATED: cake/service_test.py

So, what just happened?

- A folder named ``cake`` was created. Everything related to the ``cake`` entity lives within this folder.
- A set of python files relating to the ``cake`` entity were created
- A set of tests, relating to the ``cake`` entity were also created

If you run the ``flask routes`` command at this point, you won't see any additional routes.
This is because there's some manual wire-up that you now need to do.

TODO: 

- add wireup code
- folder structure is not correct (no `app` package)

TODO: missing requirements

- ``pip install flask_restplus``
- ``pip install sqlalchemy``

 






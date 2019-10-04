Step 2: Installing Flaskerize
=============================

We're now ready to install Flaskeriez. Let's use `pip` to do just that...

.. code-block:: bash

  pip install flaskerize

Once this command has completed we'll have installed Flaskerize along
with its dependencies. If you want to see the packages that were installed,
run the following command:

.. code-block:: bash

  pip list

This should show you something like this...

.. code-block:: bash

  $ pip list
  Package      Version
  ------------ -------
  appdirs      1.4.3
  Click        7.0
  Flask        1.1.1
  flaskerize   0.12.0
  fs           2.4.11
  itsdangerous 1.1.0
  Jinja2       2.10.1
  MarkupSafe   1.1.1
  pip          19.2.3
  pytz         2019.2
  setuptools   40.8.0
  six          1.12.0
  termcolor    1.1.0
  Werkzeug     0.16.0

.. note:: The exact versions shown here may differ from the ones you see when you install **flaskerize**.

You should now have access to the ``fz`` command, verify this with ``fz --help``, which should display something like the following:

.. code-block:: bash

  $ fz --help
  Flaskerizing...
  usage: fz [-h] {attach,bundle,generate} [{attach,bundle,generate} ...]

  positional arguments:
    {attach,bundle,generate}
                          Generate a new resource

  optional arguments:
    -h, --help            show this help message and exit

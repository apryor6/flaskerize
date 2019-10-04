Glossary of Terms
=================

.. glossary::

  entity
    An entity is a combination of a Marshmallow schema, type-annotated interface, SQLAlchemy model, Flask controller, and CRUD service.
    It also contains tests and provides functionality for being registered within an existing Flask application via its register_routes method.
    `This blog post <http://alanpryorjr.com/2019-05-20-flask-api-example/>`_  gives more details on entities.

  schematics
    Schematics generate code from parameterized templates.
    **flaskerize** ships with a bunch of built in schematics, listed `here <https://github.com/apryor6/flaskerize/tree/master/flaskerize/schematics>`_

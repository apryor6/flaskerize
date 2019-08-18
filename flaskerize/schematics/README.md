# Schematics built into flaskerize

The following is a summary/description of the various schematics that ship with `flaskerize` itself

### Entity

An `entity` is a combination of a Marshmallow schema, type-annotated interface, SQLAlchemy model, Flask controller, and CRUD service as described [in this blog post](http://alanpryorjr.com/2019-05-20-flask-api-example/). It contains tests and provides functionality for being registered within an existing Flask application via its `register_routes` method in `__init__.py.

_Additional parameters:_

- None (only uses the default/required `name` parameter)

_Example Usage_

The command `fz generate entity path/to/my/doodad` would produce an `entity` with the following directory structure.

```
path
└── to
    └── my
        └── doodad
            ├── __init__.py
            ├── controller.py
            ├── controller_test.py
            ├── interface.py
            ├── interface_test.py
            ├── model.py
            ├── model_test.py
            ├── schema.py
            ├── schema_test.py
            ├── service.py
            └── service_test.py
```

### setup

`setup` creates a `setup.py` file.

_Additional parameters:_

```
    {
      "arg": "--version",
      "type": "str",
      "default": "0.1.0",
      "help": "Current project version"
    },
    {
      "arg": "--description",
      "type": "str",
      "default": "Project built by Flaskerize",
      "help": "Project description"
    },
    {
      "arg": "--author",
      "type": "str",
      "help": "Project author"
    },
    {
      "arg": "--author-email",
      "type": "str",
      "help": "Project author"
    },
    {
      "arg": "--url",
      "type": "str",
      "default": "https://github.com/apryor6/flaskerize",
      "help": "Project website / URL"
    },
    {
      "arg": "--install-requires",
      "type": "str",
      "nargs": "+",
      "help": "Requirements"
    }
```

_Example Usage_

`fz generate setup demo/doodad`

Creates the following directory structure:

```
demo
└── setup.py
```

Where the contents of setup.py correspond to a new package named "doodad"
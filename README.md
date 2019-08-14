[![codecov](https://codecov.io/gh/apryor6/flaskerize/branch/master/graph/badge.svg)](https://codecov.io/gh/apryor6/flaskerize)
[![license](https://img.shields.io/github/license/apryor6/flaskerize)](https://img.shields.io/github/license/apryor6/flaskerize)


# flaskerize

`flaskerize` is a code generation and project modification command line interface (CLI) written in Python and created for Python. It is heavily influenced by concepts and design patterns of the [Angular CLI](https://cli.angular.io/) available in the popular JavaScript framework [Angular](https://github.com/angular). 

Use `flaskerize` for tasks including:

    - Generating Flask resources such as Dockerfiles, blueprints, SQLAlchemy entites, or even entire applications, all with functioning tests
	- Upgrading between breaking versions of projects that provide flaskerize upgrade schematics with one command
    - Bundling and serving static web applications such as Angular, React, Gatsby, Jekyll, etc within a new or existing Flask app.
    - Registering Flask resources as new routes within an existing application 
    - Creating new schematics for your own library or organization

### What about cookiecutter?

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) is awesome and does something different than `flaskerize`, but understandably they sound similar at first. Whereas `cookiecutter` is designed for scaffolding new projects, `flaskerize` is for ongoing use within an existing project for generation of new components, resources, etc and for modification of existing code.

Both projects use Jinja templates and JSON files for configuration of parameters. If you like `cookiecutter` (like me), you should feel right at home with `flaskerize`.

### Flaskerize is looking for developers!

_At the time of this writing, the `flaskerize` project is somewhat of a experiment that was born out of a personal weekend hackathon. I am pretty happy with how that turned out, particularly the CLI syntax, but there are many aspects of the current internal code that should be changed. See the Issues section for updates on this. The rest of this section details the grander vision for the project_

Currently, there is nothing even remotely close to the Angular CLI descried previously in the Python community, but we would benefit from it immensely. This is the reason for `flaskerize`. The vision is to create a generalized and extensible CLI for generation of new code and modification of existing code. This functionality could include, but is not limited to, things such as generating:

	- Flask API resources, such as those described [in this blog post](http://alanpryorjr.com/2019-05-20-flask-api-example/) (multi-file templates)
	- SQLAlchemy models
	- Marshmallow schemas
	- Typed interfaces
	- Flask/Django views and other Jinja templates
	- Data science modeling pipelines
	- Anything else the community wants to provide templates for

This last one is important, as providing a hook to make the system extensible opens an entire ecosystem of possibilities. Imagine being able to `pip install <some_custom_templates>` and then being able to use `flaskerize` to generate a bunch of custom code that is specific to your organization, personal project, enthusiast group, etc.

In addition to code generation, this CLI could modify existing files. For example -- create a new directory containing a Flask-RESTplus Namespace and associated resources, tests, _and then register that within an existing Flask app_. This would need to be able to inspect the existing app and determine if the registration has already been provided and adding it only if necessary. The magic here is that with one command the user will be able to generate a new resource, reload (or hot-reload) their app, and view the new code already wired up with working tests. I cannot emphasize enough how much this improves developer workflow, especially among teams and/or on larger projects.
  

### Why do I need a tool like this?

Productivity, consistency, and also productivity.

Flaskerize is an incredible productivity boost (_something something 10x dev_). This project is based on the concept of _schematics_, which can be used to generate code from parameterized templates. However, schematics can do much more. They support the ability to register newly created entities with other parts of the app, generate functioning tests, and provide upgrade paths across breaking version of libraries. Perhaps more important than the time this functionality saves the developer is the consistency it provides to the rest of the team, resulting in decreased time required for code reviews and collaborative development. Also, it promotes testing, which is always a good thing.


## Installation

Simple, `pip install flaskerize`

## Examples

### Create a new React + Flask project and bundle together with Flaskerize

Install [yarn](https://yarnpkg.com/lang/en/docs/install/) and [create-react-app](https://facebook.github.io/create-react-app/docs/getting-started)

Make a new react project and build into a static site:

```
create-react-app test
cd test
yarn build --prod
cd ..
```

Generate a new Flask app with `flaskerize`

`fz generate app app`

Bundle the new React and Flask apps together:

`fz bundle --from test/build/ --to app:create_app`

Run the resulting app:

`python app.py`

The app will now be available on [http:localhost:5000/](http:localhost:5000/)!

### Generate a basic Flask app

Generating a basic Flask app is simple:

`fz generate app my_app`

Then you can start the app with `python my_app.py` and navigate to http://localhost:5000/health to check that the app is online

### Create new React app

Install [yarn](https://yarnpkg.com/lang/en/docs/install/) and [create-react-app](https://facebook.github.io/create-react-app/docs/getting-started)

```
create-react-app test
cd test
yarn build --prod
cd ..
```

Upon completion the built site will be contained in `test/build/`

To view the production React app as-is (no Flask), you can use `serve` (you'll need to install it globally first `yarn global add serve`)

`serve -s test/build/`

Alternatively, you could also serve directly with python `http.server`:

`python -m http.server 5000 --directory test/build`
The app will now be available on [http:localhost:5000/](http:localhost:5000/)

Now, to serve this from a new Flask app with `flaskerize`, run the following

`fz generate app --from test/build/ app.py`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your React app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!




### Create new Angular app

Install [yarn](https://yarnpkg.com/lang/en/docs/install/) and [the Angular CLI](https://cli.angular.io/)

```
ng new
cd <project name>
yarn build --prod
fz generate app --from dist/<project name>/ app.py
```

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your Angular app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!

### Attach site to an existing Flask app

_Flaskerize uses the [factory pattern](http://flask.pocoo.org/docs/1.0/patterns/appfactories/) exclusively. If you're existing application does not follow this, see [Factory pattern](#factory-pattern)_

#### Attach with one command and generate Dockerfile

`fz bundle --from test/build/ --to app:create_app --with-dockerfile`


#### Separate generation and attachment

First, create a blueprint from the static site

`fz generate bp --from test/build/ _fz_blueprint.py`

Next, attach the blueprint to your existing Flask app

`fz a --to app.py:create_app _fz_blueprint.py`



### Schematics in third-party packages

`flaskerize` is fully extensible and supports schematics provided by external libraries. To target a schematic from another package, simply use the syntax `fz generate <package_name>:<schematic_name> [OPTIONS]`

Flaskerize expects to find a couple of things when using this syntax:

	- The package `<package_name>` should be installed from the current python environment
	- The top-level source directory of `<package_name>` should contain a `schematics/` package. Inside of that directory should be one or more directories, each corresponding to a single schematic. See the section "Structure of a schematic" for details on schematic contents.
	- A `schematics/__init__.py` file, just so that schematics can be found as a package

> For schematics that are built into `flaskerize`, you can drop the `<package_name>` piece of the schematic name. Thus the command `fz generate flaskerize:app new_app` is _exactly equivalent_ to `fz generate app new_app`. For all third-party schematics, you must provide both the package and schematic name.

For example, the command  `fz generate test_schematics:resource my/new/resource` will work if test_schematics is an installed package in the current path with a source directory structure similar to:

```
├── setup.py
└── test_schematics
    ├── __init__.py
    └── schematics
        ├── __init__.py
        ├── resource
        │   ├── schema.json
        │   ├── someConfig.json.template
        │   ├── thingy.interface.ts.template
        │   ├── thingy.py.template
        │   └── widget.py.template
```

### Structure of a schematic

#### schema.json

Each schematic contains a `schema.json` file that defines configuration parameters including the available CLI arguments, template files to include, etc.

__parameters__:
  - templateFilePatterns: array of glob patterns representing files that are to be rendered as Jinja templates
  - ignoreFilePatterns: array of glob patterns representing files that are not to be rendered as part of the schematic output, such as helper modules
  - options: array of dicts containing parameters for argument parsing with the addition of an array parameter `aliases` that is used to generate alternative/shorthand names for the command. These dicts are passed along directly to `argparse.ArgumentParser.add_argument` and thus support the same parameters. See [here](https://docs.python.org/3/library/argparse.html) for more information.

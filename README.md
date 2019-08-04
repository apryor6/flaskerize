# flaskerize

Build tool Command line interface (CLI) for Flask for tasks including:

    - Generate Flask resources such as Dockerfiles, blueprints, or even entire applications
    - Bundle and serve static web applications such as Angular or React with python APIs through a single, combined Flask app

### Why do I need a tool like this?

This project is heavily influenced by the [CLI](https://cli.angular.io/) available in the popular JavaScript framework [Angular](https://github.com/angular). There's also some other goodness added by the [Nx]((https://nx.dev/)) project, which is made by [Nrwl](https://nrwl.io/). Of particular note is the concept of schematics, which can be used to generate code from parameterized templates. However, Angular schematics can do much more. They support the ability to register newly created entities with other parts of the app, generate functioning tests, and provide upgrade paths across breaking version of libraries. Perhaps more important than the time this functionality saves the developer is the consistency it provides to the rest of the team, resulting in decreased time required for code reviews and collaborative development. Also, it promotes testing, which is always a good thing in my book.

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
  


## Installation

Simple, `pip install flaskerize`

## Examples

### Create a new React + Flask project and bundle together with Flaskerize

Install [yarn](https://yarnpkg.com/lang/en/docs/install/) and [create-react-app](https://facebook.github.io/create-react-app/docs/getting-started)

Make a new react project and build into a static site:

`create-react-app test`

`cd test`

`yarn build --prod`

`cd ..`

Generate a new Flask app with `flaskerize`

`fz g app app.py`

Bundle the new React and Flask apps together:

`fz b -from test/build/ -to app:create_app`

Run the resulting app:

`python app.py`

The app will now be available on [http:localhost:5000/](http:localhost:5000/)!

### Generate a basic Flask app

Generating a basic Flask app is simple:

`flaskerize generate hello-world app.py`

Or the shorthand:

`fz g hw app.py`

The first argument after the `generate` flag is the type of application you want to
create (see [available types](#available-types), and the following argument is the name of the application.

### Create new React app

Install [yarn](https://yarnpkg.com/lang/en/docs/install/) and [create-react-app](https://facebook.github.io/create-react-app/docs/getting-started)

`create-react-app test`

`cd test`

`yarn build --prod`

`cd ..`

To view the production React app as-is (no Flask), you can use `serve` (you'll need to install it globally first `yarn global add serve`)

`serve -s test/build/`

The app will now be available on [http:localhost:5000/](http:localhost:5000/)

Now, to serve this from a new Flask app with `flaskerize`, run the following

`flaskerize generate app -from test/build/ app.py`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your React app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!

### Create new Angular app

Install [yarn](https://yarnpkg.com/lang/en/docs/install/) and [the Angular CLI](https://cli.angular.io/)

`ng new`

`cd <project name>`

`yarn build --prod`

`flaskerize generate app -from dist/<project name>/ app.py`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your Angular app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!

### Attach site to an existing Flask app

_Flaskerize uses the [factory pattern](http://flask.pocoo.org/docs/1.0/patterns/appfactories/) exclusively. If you're existing application does not follow this, see [Factory pattern](#factory-pattern)_

#### Attach with one command and generate Dockerfile

`fz b -from test/build/ -to app:create_app --with-dockerfile`

Or, longer
`flaskerize bundle -from test/build/ -to app:create_app --with-dockerfile`

#### Separate generation and attachment

First, create a blueprint from the static site

`fz g bp -from test/build/ _fz_blueprint.py`

Next, attach the blueprint to your existing Flask app

`fz a -to app.py:create_app _fz_blueprint.py`

You can also use the longer form of both of these commands:

`flaskerize generate blueprint --static-dir-name test/build/ _fz_blueprint.py`

`flaskerize attach _fz_blueprint.py -to app:create_app`

### Generate a new namespace

Usage: `fz g ns <basename>`
Namespace generation will create a new file containing a:
	- Class
	- Marshmallow Schema
	- Flask-RESTplus Resource

The `basename` argument is used to determine the name of the classes and a default filename unless one is specified with the `-o` flag. By default, a test is also generated using the same filename as the resource except ending in `_test.py`. The generated tests using pytest and assume (currently) that you have followed the best practice of creating a tests/fixtures.py file within the app that contains pytest fixtures for generating an app, client, etc. For example, this might simply be 

```python
# app/test/fixtures.py

import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app('test')


@pytest.fixture
def client(app):
    return app.test_client()
```

_Note: The test files for the code itself are always placed alongside the code itself. For example, the test for `api/widget.py` should be `api/widget_test.py`. The `tests/` folder is for application-wide testing utilities and, although you can place tests here and they will correctly be detected and run, it is not advised. It is better to localize all code related to the same concept. If you are doubting whether you are putting code into the right place, always ask yourself "How long would it take me to delete this feature entirely from the code?". If the answer is "five seconds because I just delete the `app/doodad` folder, then you are probably doing this right."_

Example:
`fz g ns product --dry-run`

### <a name="factory-pattern"></a>Factory Pattern

WIP

### <a name="available-types"></a>Available application types

    - hello-world (hw): A basic hello world app. Args: [app_name -> name of the app]


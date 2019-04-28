# flaskerize

Build tool Command line interface (CLI) for Flask for tasks including:

    - Generate Flask resources such as Dockerfiles, blueprints, or even entire applications
    - Bundle and serve static web applications such as Angular or React with python APIs through a single, combined Flask app

## Installation

Simple, `pip install flaskerize`

## Examples

### Create a new React + Flask project with Flaskerize

Make a new react project and build into a static site:

`create-react-app test`

`cd test`

`yarn build --prod`

`cd ..`

Generate a new Flask app with `flaskerize`

`fz g app app.py`

Bundle the new React and Flask apps together:

`fz b -from test/build -to app:create_app`

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

`create-react-app test`

`cd test`

`yarn build --prod`

`cd ..`

To view the production React app as-is (no Flask), you can use `serve` (you'll need to install it globally first `yarn global add serve`)

`serve -s test/build/`

The app will now be available on [http:localhost:5000/](http:localhost:5000/)

Now, to serve this from a new Flask app with `flaskerize`, run the following

`flaskerize generate app -from ./test/build/ app.py`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your React app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!

### Create new Angular app

`ng new`

`cd <project name>`

`yarn build --prod`

`flaskerize generate app -from ./dist/<project name>/ app.py`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your Angular app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!


### Attach site to an existing Flask app

_Flaskerize uses the [factory pattern](http://flask.pocoo.org/docs/1.0/patterns/appfactories/) exclusively. If you're existing application does not follow this, see [Factory pattern](#factory-pattern)_


#### Attach with one command

`fz b -from test/build -to app:create_app`

Or, longer
`flaskerize bundle -from test/build -to app:create_app`

#### Separate generation and attachment
First, create a blueprint from the static site

`fz g bp -from test/build/ _fz_blueprint.py`

Next, attach the blueprint to your existing Flask app

`fz a -to app.py:create_app _fz_blueprint.py`

You can also use the longer form of both of these commands:

`flaskerize generate blueprint --static-dir-name test/build/ _fz_blueprint.py`

`flaskerize attach _fz_blueprint.py -to app:create_app`



### <a name="factory-pattern"></a>Factory Pattern
WIP

### <a name="available-types"></a>Available application types

    - hello-world (hw): A basic hello world app. Args: [app_name -> name of the app]



# flaskerize

Build tool Command line interface (CLI) for Flask for tasks including:

    - Generate Flask resources such as Dockerfiles, blueprints, or even entire applications
    - Bundle and serve static web applications such as Angular or React with python APIs through a single, combined Flask app

## Installation

Simple, `pip install flaskerize`

## Examples

### Generate a basic Flask app

Generating a basic Flask app is simple:

`flaskerize generate hello-world app.py`

Or the shorthand:

`flaskerize -g hw app.py`

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

`flaskerize generate from-static-dir ./test/build/ app.py`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your React app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!

### Create new Angular app

`ng new`

`cd <project name>`

`yarn build --prod`

`flaskerize generate from-static-dir ./dist/<project name>/ app.py`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your Angular app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!

## <a name="available-types"></a>Available application types

    - hello-world (hw): A basic hello world app. Args: [app_name -> name of the app]
    - from-static-dir (fsd): Serves an existing static site from Flask. Args: [static_dir_name -> name of the directory containing static site; app_name -> name of the app]

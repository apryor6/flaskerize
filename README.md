# flaskerize

Bundle and serve static web applications such as Angular or React with python APIs through a single, combined Flask app

## Installation

Simple, `pip install flaskerize`

## Examples

### Create new React app

`create-react-app test`
`cd test`
`yarn build --prod`
`cd ..`

To view the production React app as-is (no Flask), you can use `serve` (you'll need to install it globally first `yarn global add serve`)

`serve -s test/build/`

The app will now be available on [http:localhost:5000/](http:localhost:5000/)

Now, to serve this from a new Flask app with `flaskerize`, run the following

`flaskerize --init-flask=app.py ./test/build/`

This command will generate a file `app.py` containing the Flask app, which can then be run with `python app.py`

The Flask-ready version of your React app can now be viewed at [http:localhost:5000/](http:localhost:5000/)!

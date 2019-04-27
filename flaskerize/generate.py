
def _generate(contents, file, mode='w'):
    with open(file, mode) as fid:
        fid.write(contents)
    print(f"Successfully created {file}")


def _dry_run(contents, file, mode='w'):
    print(f"Successfully created {file}")


def hello_world(appname):
    print('Generating a hello_world app')

    # The routing for `send_from_directory` comes directly from https://stackoverflow.com/questions/44209978/serving-a-create-react-app-with-flask  # noqa
    CONTENTS = f"""import os
from flask import Flask, send_from_directory


app = Flask(__name__)

# Serve React App
@app.route('/')
def serve():
    return 'Hello, Flaskerize!'

if __name__ == '__main__':
    app.run()

    """
    _generate(CONTENTS, appname)
    print("Successfully created new app '{}'".format(appname))


def from_static_dir(dirname, appname):
    print('dirname = ', dirname)
    print('appname = ', appname)
    print('Generating a from_static_dir app')

    # The routing for `send_from_directory` comes directly from https://stackoverflow.com/questions/44209978/serving-a-create-react-app-with-flask  # noqa
    CONTENTS = f"""import os
from flask import Flask, send_from_directory


app = Flask(__name__, static_folder='{dirname}')

# Serve React App
@app.route('/', defaults={{'path': ''}})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()

    """
    _generate(CONTENTS, appname)
    print("Successfully created new app '{}'".format(appname))


a = {
    'hello-world': hello_world, 'hw': hello_world,
    'from_static_dir': from_static_dir, 'fsd': from_static_dir
}

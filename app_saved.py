import os
from flask import Flask, send_from_directory


def create_app():
    from _flaskerize_blueprint import site
    app = Flask(__name__, static_folder='test/build')
    print('registering')
    app.register_blueprint(site, url_prefix='/')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

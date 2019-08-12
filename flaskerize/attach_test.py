import pytest
from unittest.mock import MagicMock
from dataclasses import dataclass

from flaskerize.attach import attach


def test_flaskerize_generate():
    import os

    status = os.system("fz bundle --dry-run -from test/build/ -to app:create_app")
    assert status == 0
    assert not os.path.isfile("should_not_create.py")


def test_attach_with_dry_run(tmp_path):
    CONTENTS = """import os
    from flask import Flask

    def create_app():
        app = Flask(__name__)

        @app.route("/health")
        def serve():
            return "{{ name }} online!"

        return app

    if __name__ == "__main__":
        app = create_app()
        app.run()"""

    app_file = f"{tmp_path}/app.py"
    with open(app_file, "w") as fid:
        fid.write(CONTENTS)

    @dataclass
    class Args:
        to: str = app_file
        bp: str = "_fz_bp.py"
        dry_run: bool = True

    attach(Args())


def test_attach_without_dry_run_raises_if_file_does_not_exist(tmp_path):
    from os import path

    from flaskerize import attach

    CONTENTS = """import os
    from flask import Flask
    # a comment

    def create_app():
        app = Flask(__name__)

        @app.route("/health")
        def serve():
            return "{{ name }} online!"

        return app

    if __name__ == "__main__":
        app = create_app()
        app.run()"""

    app_file = f"{tmp_path}/app.py"
    with open(app_file, "w") as fid:
        fid.write(CONTENTS)

    @dataclass
    class Args:
        to: str = app_file
        bp: str = "_fz_bp.py"
        dry_run: bool = False

    outfile = f"{tmp_path}/outfile.py"
    attach.split_file_factory = MagicMock(return_value=(app_file, "create_app"))
    attach.attach(Args())


def test_attach_raises_with_no_target_function_call(tmp_path):
    from os import path

    from flaskerize import attach

    CONTENTS = """import os
    from flask import Flask

    def misnamed_create_app():
        app = Flask(__name__)

        @app.route("/health")
        def serve():
            return "{{ name }} online!"

        return app

    if __name__ == "__main__":
        app = create_app()
        app.run()"""

    app_file = f"{tmp_path}/app.py"
    with open(app_file, "w") as fid:
        fid.write(CONTENTS)

    @dataclass
    class Args:
        to: str = app_file
        bp: str = "_fz_bp.py"
        dry_run: bool = False

    outfile = f"{tmp_path}/outfile.py"
    attach.split_file_factory = MagicMock(return_value=(app_file, "create_app"))
    with pytest.raises(SyntaxError):
        attach.attach(Args())


def test_attach_raises_with_no_target_function_call(tmp_path):
    from os import path

    from flaskerize import attach

    CONTENTS = """import os
    from flask import Flask

    def misnamed_create_app():
        app = Flask(__name__)

        @app.route("/health")
        def serve():
            return "{{ name }} online!"

        return app

    if __name__ == "__main__":
        app = create_app()
        app.run()"""

    app_file = f"{tmp_path}/app.py"
    with open(app_file, "w") as fid:
        fid.write(CONTENTS)

    @dataclass
    class Args:
        to: str = app_file
        bp: str = "_fz_bp.py"
        dry_run: bool = False

    outfile = f"{tmp_path}/outfile.py"
    attach.split_file_factory = MagicMock(return_value=(app_file, "create_app"))
    with pytest.raises(SyntaxError):
        attach.attach(Args())


def test_attach_raises_with_no_Flask_call(tmp_path):
    from os import path

    from flaskerize import attach

    CONTENTS = """import os
    from flask import Flask

    def create_app():

        @app.route("/health")
        def serve():
            return "{{ name }} online!"

        return app

    if __name__ == "__main__":
        app = create_app()
        app.run()"""

    app_file = f"{tmp_path}/app.py"
    with open(app_file, "w") as fid:
        fid.write(CONTENTS)

    @dataclass
    class Args:
        to: str = app_file
        bp: str = "_fz_bp.py"
        dry_run: bool = False

    outfile = f"{tmp_path}/outfile.py"
    attach.split_file_factory = MagicMock(return_value=(app_file, "create_app"))
    with pytest.raises(SyntaxError):
        attach.attach(Args())

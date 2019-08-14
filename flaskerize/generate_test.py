from unittest.mock import patch, MagicMock

from dataclasses import dataclass


@patch("flaskerize.generate._generate")
def test_hello_world(_generate: MagicMock):
    from flaskerize.generate import hello_world

    @dataclass
    class Args:
        dry_run: bool = True
        output_name: str = "output_name"
        output_file: str = "output_file"

    hello_world(Args())

    _generate.assert_called_once()


@patch("flaskerize.generate._generate")
def test_app_from_dir(_generate: MagicMock):
    from flaskerize.generate import app_from_dir

    @dataclass
    class Args:
        dry_run: bool = True
        output_name: str = "output_name"
        output_file: str = "output_file"
        filename: str = "filename"
        source: str = "/path/to/source"

    app_from_dir(Args())

    _generate.assert_called_once()


@patch("flaskerize.generate._generate")
def test_wsgi(_generate: MagicMock):
    from flaskerize.generate import wsgi

    @dataclass
    class Args:
        dry_run: bool = True
        output_name: str = "output_name"
        output_file: str = "output_file"
        filename: str = "filename"
        source: str = "/path/to/source"

    wsgi(Args())

    _generate.assert_called_once()


@patch("flaskerize.generate._generate")
def test_namespace(_generate: MagicMock):
    from flaskerize.generate import namespace

    @dataclass
    class Args:
        dry_run: bool = True
        output_name: str = "output_name"
        output_file: str = "output_file"
        filename: str = "filename"
        source: str = "/path/to/source"
        without_test: bool = False

    namespace(Args())

    _generate.assert_called()


@patch("flaskerize.generate._generate")
def test_namespace_test(_generate: MagicMock):
    from flaskerize.generate import namespace_test

    @dataclass
    class Args:
        dry_run: bool = True
        output_name: str = "output_name"
        output_file: str = "output_file"
        filename: str = "filename"
        source: str = "/path/to/source"
        without_test: bool = False

    namespace_test(Args())

    _generate.assert_called()


@patch("flaskerize.generate._generate")
def test_dockerfile(_generate: MagicMock):
    from flaskerize.generate import dockerfile

    @dataclass
    class Args:
        dry_run: bool = True
        output_name: str = "output_name"
        output_file: str = "output_file"
        filename: str = "filename"
        source: str = "/path/to/source"
        without_test: bool = False

    dockerfile(Args())

    _generate.assert_called()


def test__generate_with_dry_run(tmp_path):
    from os import path

    from flaskerize.generate import _generate

    CONTENTS = "asdf"
    output_name = path.join(tmp_path, "some/file")
    _generate(contents=CONTENTS, output_name=output_name, dry_run=True)

    assert not path.isfile(output_name)


def test__generate_with_file(tmp_path):
    from os import path

    from flaskerize.generate import _generate

    CONTENTS = "asdf"
    output_name = path.join(tmp_path, "file.py")
    _generate(contents=CONTENTS, output_name=output_name, dry_run=False)

    assert path.isfile(output_name)


def test__generate_with_adds_extension(tmp_path):
    from os import path

    from flaskerize.generate import _generate

    CONTENTS = "asdf"
    output_name = path.join(tmp_path, "file")
    _generate(contents=CONTENTS, output_name=output_name, dry_run=False)

    assert path.isfile(output_name + ".py")


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


# @patch("flaskerize.generate._generate")
# def test_app(_generate: MagicMock):
#     from flaskerize.generate import app

#     app([])

#     _generate.assert_called_once()

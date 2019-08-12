from pytest import fixture
import os
from os import path
from unittest.mock import patch, MagicMock
from typing import Callable

from .render import SchematicRenderer


@fixture
def renderer(tmp_path):
    os.makedirs(f"{tmp_path}/schematics/doodad")
    return SchematicRenderer(
        schematic_path=f"{tmp_path}/schematics/doodad", root="./", dry_run=True
    )


def test__check_get_arg_parser_returns_None_with_no_file(renderer: SchematicRenderer):
    parser = renderer._check_get_arg_parser()

    assert parser is None


def test__check_get_arg_parser_returns_parser_with_schema_file(
    renderer: SchematicRenderer
):
    CONTENTS = """
    {
        "options": [
          {
            "arg": "some_option",
            "type": "str",
            "help": "An option used in this test"
          }
        ]
      }
      
    """
    schema_path = f"{renderer.schematic_path}/schema.json"
    print(f"renderer.schematic_path = {renderer.schematic_path}")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    parser = renderer._check_get_arg_parser()
    assert parser is not None


def test__check_get_arg_parser_returns_functioning_parser_with_schema_file(
    renderer: SchematicRenderer
):
    CONTENTS = """
    {
        "options": [
          {
            "arg": "some_option",
            "type": "str",
            "help": "An option used in this test"
          }
        ]
      }

    """
    schema_path = f"{renderer.schematic_path}/schema.json"
    print(f"renderer.schematic_path = {renderer.schematic_path}")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    parser = renderer._check_get_arg_parser()
    parsed = parser.parse_args(["some_value"])
    assert parsed.some_option == "some_value"


def test__get_template_files(tmp_path, renderer: SchematicRenderer):
    from pathlib import Path

    Path(path.join(renderer.schematic_path, "b.template.txt")).touch()
    Path(path.join(renderer.schematic_path, "c.notatemplate.txt")).touch()
    Path(path.join(renderer.schematic_path, "a.template.txt")).touch()

    template_files = renderer._get_template_files()
    assert len(template_files) == 2


def test__generate_outfile(renderer: SchematicRenderer):
    outfile = renderer._generate_outfile(
        template_file="my/file.template.txt", root="/base"
    )
    base, file = path.split(outfile)
    assert file == "file.txt"


@patch("flaskerize.render.colored")
class TestColorizingPrint:
    def test__print_created(self, colored: MagicMock, renderer: SchematicRenderer):
        renderer._print_created("print me!")

        colored.assert_called_once()

    def test__print_modified(self, colored: MagicMock, renderer: SchematicRenderer):
        renderer._print_modified("print me!")

        colored.assert_called_once()

    def test__print_deleted(self, colored: MagicMock, renderer: SchematicRenderer):
        renderer._print_deleted("print me!")

        colored.assert_called_once()

    def test_print_summary_with_no_updates(
        self, colored: MagicMock, renderer: SchematicRenderer
    ):
        renderer.print_summary()

        colored.assert_not_called()

    def test_print_summary_with_updates(
        self, colored: MagicMock, renderer: SchematicRenderer
    ):
        renderer._files_created.append("some file I made")
        renderer.print_summary()

        colored.assert_called_once()


@patch("flaskerize.render.colored")
def test_render(colored, renderer):
    renderer._get_template_files = lambda: ["file1"]
    mock = MagicMock()
    renderer.render_from_file = mock

    renderer.render(name="test_resource", args=[])

    mock.assert_called_once()
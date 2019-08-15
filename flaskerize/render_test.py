from pytest import fixture, raises
import os
from os import path
from unittest.mock import patch, MagicMock
from typing import Callable

from .render import SchematicRenderer


@fixture
def renderer(tmp_path):
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    return SchematicRenderer(
        schematic_path=path.join(tmp_path, "schematics/doodad"), root="./", dry_run=True
    )


def test__check_get_arg_parser_returns_parser_with_schema_file(
    renderer: SchematicRenderer
):
    CONTENTS = """
    {
        "templateFilePatterns": ["**/*.template"],
        "options": [
          {
            "arg": "some_option",
            "type": "str",
            "help": "An option used in this test"
          }
        ]
    }
      
    """
    schema_path = path.join(renderer.schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    parser = renderer._check_get_arg_parser(schema_path)
    assert parser is not None


def test__check_get_arg_parser_returns_functioning_parser_with_schema_file(
    renderer: SchematicRenderer
):
    CONTENTS = """
    {
        "templateFilePatterns": ["**/*.template"],
        "options": [
          {
            "arg": "some_option",
            "type": "str",
            "help": "An option used in this test"
          }
        ]
    }

    """
    schema_path = path.join(renderer.schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    parser = renderer._check_get_arg_parser(schema_path)
    assert parser is not None
    parsed = parser.parse_args(["some_value"])
    assert parsed.some_option == "some_value"


def test_get_template_files(tmp_path):
    from pathlib import Path

    CONTENTS = """
    {
        "templateFilePatterns": ["**/*.template"],
        "options": []
    }
      
    """
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    Path(path.join(renderer.schematic_path, "b.txt.template")).touch()
    Path(path.join(renderer.schematic_path, "c.notatemplate.txt")).touch()
    Path(path.join(renderer.schematic_path, "a.txt.template")).touch()

    template_files = renderer.get_template_files()

    assert len(template_files) == 2


def test_ignoreFilePatterns_is_respected(tmp_path):
    from pathlib import Path

    CONTENTS = """
    {
        "templateFilePatterns": ["**/*.template"],
        "ignoreFilePatterns": ["**/b.txt.template"],
        "options": []
    }
      
    """
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    Path(path.join(renderer.schematic_path, "b.txt.template")).touch()
    Path(path.join(renderer.schematic_path, "c.notatemplate.txt")).touch()
    Path(path.join(renderer.schematic_path, "a.txt.template")).touch()

    template_files = renderer.get_template_files()

    assert len(template_files) == 1


def test__generate_outfile(renderer: SchematicRenderer):

    outfile = renderer._generate_outfile(
        template_file="my/file.txt.template", root="/base"
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
        renderer._files_modified.append("some file I modified")
        renderer._files_deleted.append("some file I deleted")
        renderer._directories_created.append("some directory I made/")
        renderer.print_summary()

        assert colored.call_count == 4


@patch("flaskerize.render.colored")
def test_render(colored, renderer):
    renderer.get_template_files = lambda: ["file1"]
    mock = MagicMock()
    renderer.render_from_file = mock

    renderer.render(name="test_resource", args=[])

    mock.assert_called_once()


def test_render_from_file(renderer, tmp_path):
    filename = os.path.join(tmp_path, "my_template.py.template")
    CONTENTS = "{{ secret }}"
    with open(filename, "w") as fid:
        fid.write(CONTENTS)
    outfile = os.path.join(tmp_path, "doodad/my_template.py")
    renderer._generate_outfile = MagicMock(return_value=outfile)
    renderer.render_from_file(filename, context={"secret": "42"})

    assert len(renderer._directories_created) > 0


def test_render_from_file_when_outfile_exists(renderer, tmp_path):
    filename = os.path.join(tmp_path, "my_template.py.template")
    CONTENTS = "{{ secret }}"
    with open(filename, "w") as fid:
        fid.write(CONTENTS)
    outdir = os.path.join(tmp_path, "doodad")
    os.makedirs(outdir)
    outfile = os.path.join(outdir, "my_template.py")
    with open(outfile, "w") as fid:
        fid.write("some existing content")
    renderer._generate_outfile = MagicMock(return_value=outfile)
    renderer.render_from_file(filename, context={"secret": "42"})

    assert len(renderer._files_modified) > 0


def test__load_run_function_raises_if_colliding_parameter_provided(tmp_path):
    CONTENTS = """
    {
        "options": [
          {
            "arg": "name",
            "type": "str",
            "help": "An option that is reserved and will cause an error"
          }
        ]
    }

    """
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    with raises(ValueError):
        renderer.render(name="test_resource", args=["test_name"])


def test__load_run_function_raises_if_invalid_run_py(tmp_path):
    SCHEMA_CONTENTS = """{"options": []}"""
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(SCHEMA_CONTENTS)

    RUN_CONTENTS = """from typing import Any, Dict

from flaskerize import SchematicRenderer


def wrong_named_run(renderer: SchematicRenderer, context: Dict[str, Any]) -> None:
    return
"""
    run_path = path.join(schematic_path, "run.py")
    with open(run_path, "w") as fid:
        fid.write(RUN_CONTENTS)

    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    with raises(ValueError):
        renderer._load_run_function(
            run_function_path=path.join(renderer.schematic_path, "run.py")
        )


def test__load_run_function_uses_custom_run(tmp_path):
    SCHEMA_CONTENTS = """{"options": []}"""
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(SCHEMA_CONTENTS)

    RUN_CONTENTS = """from typing import Any, Dict

from flaskerize import SchematicRenderer


def run(renderer: SchematicRenderer, context: Dict[str, Any]) -> None:
    return "result from the custom run function"
"""
    run_path = path.join(schematic_path, "run.py")
    with open(run_path, "w") as fid:
        fid.write(RUN_CONTENTS)

    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    run = renderer._load_run_function(
        run_function_path=path.join(renderer.schematic_path, "run.py")
    )

    result = run(renderer=renderer, context={})

    assert result == "result from the custom run function"


def test__load_run_function_uses_custom_run_with_context_correctly(tmp_path):
    SCHEMA_CONTENTS = """{"options": []}"""
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(SCHEMA_CONTENTS)

    RUN_CONTENTS = """from typing import Any, Dict

from flaskerize import SchematicRenderer


def run(renderer: SchematicRenderer, context: Dict[str, Any]) -> None:
    return context["value"]
"""
    run_path = path.join(schematic_path, "run.py")
    with open(run_path, "w") as fid:
        fid.write(RUN_CONTENTS)

    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    run = renderer._load_run_function(
        run_function_path=path.join(renderer.schematic_path, "run.py")
    )

    result = run(renderer=renderer, context={"value": "secret password"})

    assert result == "secret password"


@patch("flaskerize.render.default_run")
def test_default_run_executed_if_no_custom_run(mock: MagicMock, tmp_path):
    SCHEMA_CONTENTS = """{"options": []}"""
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(SCHEMA_CONTENTS)
    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)

    renderer.render(name="test_resource", args=[])

    mock.assert_called_once()

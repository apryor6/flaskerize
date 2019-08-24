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
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schematic_files_path = path.join(schematic_path, "files/")
    os.makedirs(schematic_files_path)
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    Path(path.join(schematic_files_path, "b.txt.template")).touch()
    Path(path.join(schematic_files_path, "c.notatemplate.txt")).touch()
    Path(path.join(schematic_files_path, "a.txt.template")).touch()

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
    schematic_path = path.join(tmp_path, "schematics/doodad")
    schematic_files_path = path.join(schematic_path, "files")
    os.makedirs(schematic_files_path)
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(CONTENTS)
    renderer = SchematicRenderer(schematic_path=schematic_path, root="./", dry_run=True)
    Path(path.join(schematic_files_path, "b.txt.template")).touch()
    Path(path.join(schematic_files_path, "c.notatemplate.txt")).touch()
    Path(path.join(schematic_files_path, "a.txt.template")).touch()

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

        # One extra call if dry run is enabled
        colored.call_count == int(renderer.dry_run)

    def test_print_summary_with_updates(
        self, colored: MagicMock, renderer: SchematicRenderer
    ):
        renderer._files_created.append("some file I made")
        renderer._files_modified.append("some file I modified")
        renderer._files_deleted.append("some file I deleted")
        renderer._directories_created.append("some directory I made/")
        renderer.print_summary()

        # One extra call if dry run is enabled
        assert colored.call_count >= 4 + int(renderer.dry_run)


@patch("flaskerize.render.colored")
def test_render_colored(colored, renderer):
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


def test_copy_static_file_dry_run(renderer, tmp_path):
    filename = os.path.join(tmp_path, "my_file.txt")
    CONTENTS = "some static content"
    with open(filename, "w") as fid:
        fid.write(CONTENTS)
    outfile = os.path.join(tmp_path, "doodad/my_file.txt")
    renderer._generate_outfile = MagicMock(return_value=outfile)
    renderer.copy_static_file(filename, context={})

    assert len(renderer._files_created) > 0


def test_copy_static_file(tmp_path):
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    renderer = SchematicRenderer(
        schematic_path=path.join(tmp_path, "schematics/doodad"),
        root=path.join(tmp_path, "out/path"),
    )

    filename = os.path.join(tmp_path, "my_file.txt")
    CONTENTS = "some static content"
    with open(filename, "w") as fid:
        fid.write(CONTENTS)
    outfile = os.path.join(tmp_path, "doodad/my_file.txt")
    renderer._get_rel_path = MagicMock(return_value=outfile)
    renderer.copy_static_file(filename, context={})

    assert len(renderer._files_created) > 0
    assert os.path.exists(outfile)


def test_copy_static_file_modifies_file_if_exists(tmp_path):
    os.makedirs(path.join(tmp_path, "schematics/doodad"))
    renderer = SchematicRenderer(
        schematic_path=path.join(tmp_path, "schematics/doodad"),
        root=path.join(tmp_path, "out/path"),
    )

    filename = os.path.join(tmp_path, "my_file.txt")
    CONTENTS = "some static content"
    with open(filename, "w") as fid:
        fid.write(CONTENTS)
    outfile = os.path.join(path.join(tmp_path, "out/path"), "doodad/my_file.txt")
    os.makedirs(path.join(tmp_path, "out/path/doodad"))
    with open(outfile, "w") as fid:
        fid.write(CONTENTS)
    renderer._get_rel_path = MagicMock(return_value=outfile)
    renderer.copy_static_file(filename, context={})

    assert len(renderer._files_created) == 0
    assert len(renderer._files_modified) == 1
    assert os.path.exists(outfile)


def test_render_from_file_when_outfile_exists(renderer, tmp_path):
    filename = os.path.join(tmp_path, "my_template.py.template")
    CONTENTS = "some existing content"
    with open(filename, "w") as fid:
        fid.write(CONTENTS)
    outdir = os.path.join(tmp_path, "doodad")
    os.makedirs(outdir)
    outfile = os.path.join(outdir, "my_template.py")
    with open(outfile, "w") as fid:
        fid.write(CONTENTS)
    renderer._generate_outfile = MagicMock(return_value=outfile)
    renderer.render_from_file(filename, context={"secret": "42"})

    assert len(renderer._files_modified) > 0


def test_run_with_static_files(renderer, tmp_path):
    from flaskerize.render import default_run

    filename = os.path.join(renderer.schematic_files_path, "my_file.txt")
    os.makedirs(renderer.schematic_files_path)
    CONTENTS = "some existing content"
    with open(filename, "w") as fid:
        fid.write(CONTENTS)
    outdir = os.path.join(tmp_path, "doodad")
    outfile = os.path.join(outdir, "my_file.txt")

    renderer._generate_outfile = MagicMock(return_value=outfile)
    default_run(renderer=renderer, context={})

    assert len(renderer._files_created) > 0


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
        renderer._load_run_function(path=path.join(renderer.schematic_path, "run.py"))


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
    run = renderer._load_run_function(path=path.join(renderer.schematic_path, "run.py"))

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
    run = renderer._load_run_function(path=path.join(renderer.schematic_path, "run.py"))

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


def test_render(tmp_path: str):
    schematic_path = path.join(tmp_path, "schematic/doodad")
    schematic_files_path = path.join(schematic_path, "files")
    os.makedirs(schematic_files_path)
    SCHEMA_CONTENTS = """
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
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(SCHEMA_CONTENTS)

    TEMPLATE_CONTENT = "Hello {{ some_option }}!"
    template_path = path.join(schematic_files_path, "output.txt.template")
    with open(template_path, "w") as fid:
        fid.write(TEMPLATE_CONTENT)

    renderer = SchematicRenderer(
        schematic_path=schematic_path,
        root=path.join(tmp_path, "results"),
        dry_run=False,
    )
    renderer.render(name="Test schematic", args=["there"])

    outfile = path.join(tmp_path, "results/output.txt")
    assert path.exists(outfile)
    with open(outfile, "r") as fid:
        contents = fid.read()
    assert contents == "Hello there!"


def test_render_with_custom_function(tmp_path: str):

    schematic_path = path.join(tmp_path, "schematic/doodad")
    schematic_files_path = path.join(schematic_path, "files")
    os.makedirs(schematic_files_path)
    SCHEMA_CONTENTS = """
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
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(SCHEMA_CONTENTS)

    CUSTOM_FUNCTIONS_CONTENTS = """from flaskerize import register_custom_function  # noqa


@register_custom_function
def derp_case(val: str) -> str:
    from itertools import zip_longest

    downs = val[::2].lower()
    ups = val[1::2].upper()
    result = ""
    for i, j in zip_longest(downs, ups):
        if i is not None:
            result += i
        if j is not None:
            result += j
    return result

    """
    custom_functions_path = path.join(schematic_path, "custom_functions.py")
    with open(custom_functions_path, "w") as fid:
        fid.write(CUSTOM_FUNCTIONS_CONTENTS)

    TEMPLATE_CONTENT = "Hello {{ derp_case(some_option) }}!"
    template_path = path.join(schematic_files_path, "output.txt.template")
    with open(template_path, "w") as fid:
        fid.write(TEMPLATE_CONTENT)

    renderer = SchematicRenderer(
        schematic_path=schematic_path,
        root=path.join(tmp_path, "results"),
        dry_run=False,
    )
    renderer.render(name="Test schematic", args=["there"])

    outfile = path.join(tmp_path, "results/output.txt")
    assert path.exists(outfile)
    with open(outfile, "r") as fid:
        contents = fid.read()
    assert contents == "Hello tHeRe!"


def test_render_with_custom_function_parameterized(tmp_path: str):

    schematic_path = path.join(tmp_path, "schematic/doodad")
    schematic_files_path = path.join(schematic_path, "files")
    os.makedirs(schematic_files_path)
    SCHEMA_CONTENTS = """
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
    schema_path = path.join(schematic_path, "schema.json")
    with open(schema_path, "w") as fid:
        fid.write(SCHEMA_CONTENTS)

    CUSTOM_FUNCTIONS_CONTENTS = """from flaskerize import register_custom_function  # noqa


@register_custom_function
def truncate(val: str, max_length: int) -> str:
    return val[:max_length]

    """
    custom_functions_path = path.join(schematic_path, "custom_functions.py")
    with open(custom_functions_path, "w") as fid:
        fid.write(CUSTOM_FUNCTIONS_CONTENTS)

    TEMPLATE_CONTENT = "Hello {{ truncate(some_option, 2) }}!"
    template_path = path.join(schematic_files_path, "output.txt.template")
    with open(template_path, "w") as fid:
        fid.write(TEMPLATE_CONTENT)

    renderer = SchematicRenderer(
        schematic_path=schematic_path,
        root=path.join(tmp_path, "results"),
        dry_run=False,
    )
    renderer.render(name="Test schematic", args=["there"])

    outfile = path.join(tmp_path, "results/output.txt")
    assert path.exists(outfile)
    with open(outfile, "r") as fid:
        contents = fid.read()
    assert contents == "Hello th!"


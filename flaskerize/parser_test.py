import pytest
import os

from flaskerize.exceptions import InvalidSchema
from flaskerize.parser import FzArgumentParser


def test_flaskerize_generate():

    status = os.system("fz generate --dry-run app my/test/app")
    assert status == 0
    assert not os.path.isfile("should_not_create.py")


def test__load_schema(tmp_path):
    from flaskerize.parser import _load_schema

    CONTENTS = """{"wrong_key":[]}"""
    schematic_dir = os.path.join(tmp_path, "schematics/test_schema")
    schema_filename = os.path.join(schematic_dir, "schema.json")
    os.makedirs(schematic_dir)
    with open(schema_filename, "w") as fid:
        fid.write(CONTENTS)
    with pytest.raises(InvalidSchema):
        cfg = _load_schema(schema_filename)


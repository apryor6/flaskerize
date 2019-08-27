import os


def test_schematic_from_Flaskerize(tmp_path):
    from flaskerize.parser import Flaskerize

    assert Flaskerize(f"fz generate schematic {tmp_path}".split())

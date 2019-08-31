import os


def test_schematic_from_Flaskerize(tmp_path):
    from flaskerize.parser import Flaskerize

    assert Flaskerize(
        f"fz generate schematic --from-dir {tmp_path} test_schematic".split()
    )

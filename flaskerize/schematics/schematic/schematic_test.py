import os


def test_schematic_from_Flaskerize():
    from flaskerize.parser import Flaskerize

    assert Flaskerize("fz generate schematic ./bla/schematic/test".split())

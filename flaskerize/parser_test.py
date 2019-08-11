def test_flaskerize_generate():
    import os

    status = os.system("flaskerize generate --dry-run app my/test/app")
    assert status == 0


def test_dry_run():
    import os

    status = os.system("fz generate --dry-run app my/test/app")
    assert status == 0
    assert not os.path.isfile("should_not_create.py")

def test_flaskerize_generate():
    import os
    status = os.system('flaskerize generate --dry-run hw should_not_create.py')
    assert status == 0


def test_flaskerize_g():
    import os
    status = os.system('flaskerize g --dry-run hw should_not_create.py')
    assert status == 0


def test_fz_g():
    import os
    status = os.system('fz g --dry-run hw should_not_create.py')
    assert status == 0


def test_dry_run():
    import os
    status = os.system('fz g --dry-run hw should_not_create.py')
    assert status == 0
    assert not os.path.isfile('should_not_create.py')

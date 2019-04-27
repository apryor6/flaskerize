def test_generate():
    import os
    status = os.system('flaskerize --dry-run -g hw should_not_create.py')
    assert status == 0


def test_dry_run():
    import os
    status = os.system('flaskerize --dry-run -g hw should_not_create.py')
    assert status == 0
    assert not os.path.isfile('should_not_create.py')

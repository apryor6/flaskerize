def test_generate():
    import os
    status = os.system('flaskerize --dry-run -g hw test')
    assert status == 0

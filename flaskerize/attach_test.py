def test_flaskerize_generate():
    import os

    status = os.system("fz bundle --dry-run -from test/build/ -to app:create_app")
    assert status == 0
    assert not os.path.isfile("should_not_create.py")

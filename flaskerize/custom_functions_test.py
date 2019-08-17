from flaskerize import register_custom_function


def test_register_custom_function():
    def f1():
        return 1

    @register_custom_function
    def f2():
        return 42

    assert len(register_custom_function.funcs) == 1
    assert register_custom_function.funcs[0]() == f2()
    assert register_custom_function.funcs[0]() != f1()

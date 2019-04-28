def split_file_factory(path, delim=':', default_func_name='create_app'):
    import os

    if delim in path:
        _split = path.split(delim)
        if len(_split) != 2:
            raise ValueError('Failure to parse path to app factory. Syntax should be '
                             'filename:function_name')
        filename, func = _split
    else:
        filename = path
        func = default_func_name
    if os.path.isfile(f"{filename}.py"):
        filename += '.py'
    if os.path.isdir(filename):
        if os.path.isfile(filename + '/__init__.py'):
            filename += '/__init__.py'
        else:
            raise SyntaxError(
                f"Unable to parse factory input. Input file '{filename}' is a "
                "directory, but not a package.")
    return filename, func

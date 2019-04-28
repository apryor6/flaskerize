def attach(args):
    print('Attaching...')
    # TODO: Check that the provided blueprint exists, error if not
    filename, func = _split_file_factory(args.to)
    key_lines = _find_key_lines(filename, func)
    with open(filename, 'r') as fid:
        contents = fid.read().splitlines()

    # TODO: remove the need for this check by enabling an existing static dir (see #3)
    # (https://github.com/apryor6/flaskerize/issues/3)
    indent = ' ' * 4  # TODO: dynamically determine indentation
    new_static = ", static_folder='test/build/'"

    # TODO: Verify that the flask line is greater than start_func or, more rigorously,
    # make sure that you are inserting from back to front so that the line numbers are
    # not perturbed as you go
    call_to_Flask = [c.strip() for c in contents[key_lines['flask']][:-1].split(',')]

    # TODO: fix this hardcoded path
    # updated = call_to_Flask[:-1] + f", static_folder='{static_folder}'"
    # TODO: Clean up this messy logic that is simply checking if the static_folder you
    # want to add is already present
    updated = ', '.join(
        i.strip() for i in call_to_Flask if 'static_folder' not in i) + new_static
    if (any("static_folder" in c for c in call_to_Flask)
            and updated.strip() != ', '.join(call_to_Flask).strip()):
        print("WARNING! Flaskerize does not currently support apps with "
              "existing static folders and is overwriting.")
    contents[key_lines['flask']] = f"{indent}{updated})"

    register_line = f"{indent}app.register_blueprint(site, url_prefix='/')"
    if register_line not in contents:
        contents.insert(key_lines['flask'] + 1,
                        register_line)

    import_bp_line = f"{indent}from {args.bp.replace('.py', '')} import site"
    if import_bp_line not in contents:
        contents.insert(key_lines['start_func'] + 1,
                        import_bp_line)

    contents = '\n'.join(contents)
    if args.dry_run:
        print('Dry run result: ')
        print(contents)
    else:
        with open(filename, 'w') as fid:
            fid.write(contents)


def _find_key_lines(filename, func):
    TOKEN_START_FUNC = f'def {func}'
    TOKEN_FLASK = 'Flask('
    results = {}
    with open(filename, 'r') as fid:
        for num, line in enumerate(fid):
            if TOKEN_START_FUNC in line:
                results['start_func'] = num
            if TOKEN_FLASK in line:
                results['flask'] = num
    if not results.get('start_func', None):
        raise SyntaxError(
            f"The provided factory '{func}' was not found in file '{filename}'")
    if not results.get('flask', None):
        raise SyntaxError(
            f"No call to Flask was found in the provided file '{filename}'."
            "Is your app factory setup correctly?")
    return results


def _split_file_factory(path, delim=':', default_func_name='create_app'):
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

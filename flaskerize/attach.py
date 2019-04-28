def attach(args):
    print('Attaching...')
    filename, func = _split_file_factory(args.to)
    key_lines = _find_key_lines(filename, func)
    with open(filename, 'r') as fid:
        contents = fid.read().splitlines()

    # TODO: remove the need for this check by enabling an existing static dir (see #3)
    # (https://github.com/apryor6/flaskerize/issues/3)
    if "static_folder" in contents[key_lines['flask']]:
        raise ValueError("Sorry, flaskerize does not currently support apps with "
                         "existing static folders.")

    # TODO: Verify that the flask line is greater than start_func or, more rigorously,
    # make sure that you are inserting from back to front so that the line numbers are
    # not perturbed as you go
    call_to_Flask = contents[key_lines['flask']]
    # TODO: fix this hardcoded path
    # updated = call_to_Flask[:-1] + f", static_folder='{static_folder}'"
    updated = call_to_Flask[:-1] + f", static_folder='test/build/)'"
    contents.insert(key_lines['flask'], updated)
    contents.insert(key_lines['start_func'] + 1,
                    "app.register_blueprint(site, url_prefix='/')")
    contents.insert(key_lines['start_func'] + 1,
                    "from _flaskerize_blueprint import site")


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


def _split_file_factory(path, delim=':', default_func_name='create_app'):
    if delim in path:
        _split = path.split(delim)
        if len(_split) != 2:
            raise ValueError('Failure to parse path to app factory. Syntax should be '
                             'filename:function_name')
        filename, func = _split
    else:
        filename = path
        func = default_func_name
    return filename, func

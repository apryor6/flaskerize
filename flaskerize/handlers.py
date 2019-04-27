def handle_bundle(args):
    target = args.bundle[0]
    if not target.endswith('/'):
        print("WARNING: Provided path '{}' does not end with "
              "'/', adding for you.".format(target))
        target += '/'


def handle_generate(args):
    from flaskerize import generate
    if args.dry_run:
        generate._generate = generate._dry_run
    import os
    print('generate args = ', args.generate)
    if len(args.generate) < 2:
        raise SyntaxError("ERROR: Invalid syntax found for generate. "
                          "Correct usage is `flaskerize --generate type [args]`")
    what, *called = args.generate

    if os.path.isfile(called[-1]) and not args.force:
        raise FileExistsError("ERROR: Target file '{}' already exists. "
                              "Add --force to override".format(called[-1]))
    generate.a[what](*called)

import argparse
import sys

arg_parser = argparse.ArgumentParser(description='Flaskerize')
arg_parser.add_argument('--bundle', '-b', type=str, nargs='+',
                        help='Target static site to host within Flask')
arg_parser.add_argument('--generate', '-g', type=str, nargs='+',
                        help='Generate a new resource')
arg_parser.add_argument('--force', '-f', action="store_true",
                        help='Ignore safety checks, such as checking that '
                        'target Flask app is a *.py')
arg_parser.add_argument('--dry-run', action="store_true",
                        help="Dry run -- don't actually create any files.")


def parse(args):
    return arg_parser.parse_args(args)


class FzArgumentParser(argparse.ArgumentParser):
    """Flaskerize argument parser with default common options"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument('--force', '-f', action="store_true",
                          help='Ignore safety checks, such as checking that '
                          'target Flask app is a *.py')
        self.add_argument('--dry-run', action="store_true",
                          help="Dry run -- don't actually create any files.")


class Flaskerize(object):
    COMMANDS = ['bundle', 'generate']

    def __init__(self, args):
        parser = FzArgumentParser(
            description='Build tool Command line interface (CLI) for Flask',
            usage='''flaskerize <command> [<args>]
            '''
        )
        parser.add_argument('command', help='Subcommand to run')
        parsed = parser.parse_args(args[1:2])
        if not hasattr(self, parsed.command):
            self._exit_invalid(
                parser,
                msg='ERROR: Unrecognized command. Options are {}'.format(self.COMMANDS)
            )
        getattr(self, parsed.command)(args[2:])

    def _exit_invalid(self, parser, msg=None):
        if msg:
            print(msg)
        parser.print_help()
        exit(1)

    def bundle(self, args):
        arg_parser = FzArgumentParser(description='bundle')
        arg_parser.add_argument('target', type=str,
                                help='Target static site to host within Flask')

        args = arg_parser.parse_args(args)
        target = args.target
        if not target.endswith('/'):
            print("WARNING: Provided path '{}' does not end with "
                  "'/', adding for you.".format(target))
            target += '/'
        raise NotImplementedError

    def generate(self, args):
        from flaskerize import generate
        import os

        arg_parser = FzArgumentParser(description='generate')
        arg_parser.add_argument('what', type=str,
                                help='What to generate')
        arg_parser.add_argument('output_name', type=str,
                                help='Base name for outputted resource')
        arg_parser.add_argument('-dir', '--static-dir-name', type=str,
                                help='Base name for outputted resource')
        parsed = arg_parser.parse_args(args)
        print('generate args = ', parsed)
        what = parsed.what
        output_name = parsed.output_name
        if os.path.isfile(output_name) and not parsed.force:
            raise FileExistsError("ERROR: Target file '{}' already exists. "
                                  "Add --force to override".format(output_name))
        generate.a[what](parsed)

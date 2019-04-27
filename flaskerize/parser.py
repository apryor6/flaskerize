import argparse

arg_parser = argparse.ArgumentParser(description='Flaskerize')
arg_parser.add_argument('--bundle', '-b', type=str, nargs='+',
                        help='Target static site to host within Flask')
arg_parser.add_argument('--generate', '-g', type=str, nargs='+',
                        help='Generate a new resource')
arg_parser.add_argument('--force', '-f', action="store_true",
                        help='Ignore safety checks, such as checking that '
                        'target Flask app is a *.py')


def parse(args):
    return arg_parser.parse_args(args)

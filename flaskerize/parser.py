import os
from os import path
import argparse
import sys
from typing import Any, Dict, List, Tuple, Optional


# global_arg_parser = from_schema(global_schema)
# schematic_arg_parser = from_schema("global/schema.json")
# arg_parser = global_arg_parser
# # arg_parser = argparse.ArgumentParser([global_arg_parser, schematic_arg_parser])

# arg_parser = argparse.ArgumentParser(description="Flaskerize")
# arg_parser.add_argument(
#     "--bundle",
#     "-b",
#     type=str,
#     nargs="+",
#     help="Target static site to host within Flask",
# )
# arg_parser.add_argument(
#     "--generate", "-g", type=str, nargs="+", help="Generate a new resource"
# )
# arg_parser.add_argument(
#     "--force",
#     "-f",
#     action="store_true",
#     help="Ignore safety checks, such as checking that " "target Flask app is a *.py",
# )
# arg_parser.add_argument(
#     "--dry-run", action="store_true", help="Dry run -- don't actually create any files."
# )


def _convert_types(cfg: Dict) -> Dict:
    for option in cfg["options"]:
        if "type" in option:
            option["type"] = _translate_type(option["type"])
    return cfg


def _translate_type(key: str) -> type:
    """Convert type name from JSON schema to corresponding Python type"""

    type_map: Dict[str, type] = {"str": str}
    return type_map[key]


def _load_schema(filename: str) -> Dict:
    import json

    from .exceptions import InvalidSchema

    with open(filename, "r") as fid:
        cfg = json.load(fid)
    if "options" not in cfg:
        raise InvalidSchema(f"Required key 'options' not found in '{filename}'")

    cfg = _convert_types(cfg)
    return cfg


# def _from_schema(filename: str) -> argparse.ArgumentParser:
#     """Create an argument parser from a schema JSON file"""

#     cfg = _load_schema(filename)
#     arg_parser = argparse.ArgumentParser(description="Flaskerize")
#     for option in cfg["options"]:
#         arg_parser.add_argument(
#             "--dry-run",
#             action="store_true",
#             help="Dry run -- don't actually create any files.",
#         )
#     return arg_parser


def parse(args):
    return arg_parser.parse_args(args)


class FzArgumentParser(argparse.ArgumentParser):
    """Flaskerize argument parser with default common options"""

    def __init__(self, schema: str, xtra_schema_files: Optional[List[str]] = None):
        import json

        super().__init__()
        cfgs: List[Dict] = [_load_schema(schema)]
        if xtra_schema_files:
            cfgs.extend([_load_schema(file) for file in xtra_schema_files])

        for cfg in cfgs:
            for option in cfg["options"]:
                switches = [option.pop("arg")] + option.pop("aliases", [])
                self.add_argument(*switches, **option)


# class FzGenerateParser(FzArgumentParser):
#     """Flaskerize argument parser for generate command"""

#     _GLOBAL_SCHEMA = os.path.join(os.path.dirname(__file__), "global/generate.json")


class Flaskerize(object):
    def __init__(self, args):
        import os

        dirname = os.path.dirname(__file__)
        parser = FzArgumentParser(
            os.path.join(os.path.dirname(__file__), "global/schema.json")
        )
        parsed = parser.parse_args(args[1:2])
        getattr(self, parsed.command[0])(args[2:])

    def _exit_invalid(self, parser, msg: Optional[str] = None):
        if msg:
            print(msg)
        parser.print_help()
        exit(1)

    # def attach(self, args):
    #     from flaskerize.attach import attach

    #     arg_parser = FzArgumentParser(description="attach [a]")
    #     arg_parser.add_argument(
    #         "-to",
    #         type=str,
    #         required=True,
    #         help="Flask app factory function to attach blueprint",
    #     )
    #     arg_parser.add_argument("bp", type=str, help="Blueprint to attach")
    #     parse = arg_parser.parse_args(args)
    #     attach(parse)

    # def bundle(self, args):
    #     """
    #     Generate a new Blueprint from a source static site and attach it
    #     to an existing Flask application
    #     """
    #     import os

    #     DEFAULT_BP_NAME = "_fz_bp.py"
    #     DEFAULT_WSGI_NAME = "wsgi.py"
    #     DEFAULT_GUNICORN_ENTRY = f"{DEFAULT_WSGI_NAME.replace('.py', '')}:app"

    #     arg_parser = FzArgumentParser(description="bundle [b]")
    #     arg_parser.add_argument(
    #         "-from", "--source", type=str, help="Path of input static site to bundle"
    #     )
    #     arg_parser.add_argument(
    #         "-to",
    #         type=str,
    #         required=True,
    #         help="Flask app factory function to attach blueprint",
    #     )
    #     arg_parser.add_argument(
    #         "--with-wsgi",
    #         action="store_true",
    #         help="Also generate a wsgi.py for gunicorn",
    #     )
    #     arg_parser.add_argument(
    #         "--with-dockerfile", action="store_true", help="Also generate a Dockerfile"
    #     )
    #     parsed = arg_parser.parse_args(args)
    #     if parsed.force:
    #         force = "--force"
    #     else:
    #         force = ""

    #     if parsed.source and not parsed.source.endswith("/"):
    #         print(
    #             f"Input source {parsed.source} does not end with trailing /, adding "
    #             "for you"
    #         )
    #         parsed.source += "/"
    #     self.generate(
    #         f"blueprint -from {parsed.source} {DEFAULT_BP_NAME} {force}".split()
    #     )
    #     self.attach(f"-to {parsed.to} {DEFAULT_BP_NAME} {force}".split())

    #     # Build a WSGI file if requested or needed. If user has requested a Dockerfile
    #     # without adding --with-wsgi flaskerize will add one unless a wsgi.py exists
    #     # already
    #     if parsed.with_wsgi or (
    #         parsed.with_dockerfile and not os.path.isfile(f"{DEFAULT_WSGI_NAME}")
    #     ):
    #         self.generate(f"wsgi -from {parsed.to} {DEFAULT_WSGI_NAME} {force}".split())

    #     if parsed.with_dockerfile:
    #         self.generate(
    #             f"dockerfile Dockerfile {force} -from {DEFAULT_GUNICORN_ENTRY}".split()
    #         )

    def generate(self, args):
        import os

        arg_parser = FzArgumentParser(
            schema=os.path.join(os.path.dirname(__file__), "global/generate.json")
        )
        parsed, rest = arg_parser.parse_known_args(args)
        print(f"parsed = {parsed}")
        schematic = parsed.schematic
        self._check_render_schematic(schematic, rest)

    def _split_pkg_schematic(
        self, pkg_schematic: str, delim: str = ":"
    ) -> Tuple[str, str]:
        if delim not in pkg_schematic:
            # Assume Flaskerize is the parent package and user has issued shorthand
            pkg = "flaskerize"
            schematic = pkg_schematic
        else:
            pkg, _, schematic = pkg_schematic.rpartition(delim)
            if not pkg or not schematic:
                raise ValueError(
                    f"Unable to parse schematic '{pkg_schematic}.'"
                    "Correct syntax is <package_name>:<schematic_name>"
                )
        return pkg, schematic

    def _check_validate_package(self, pkg: str) -> importlib.ModuleSpec:
        from importlib.util import find_spec

        spec = find_spec(pkg)
        if spec is None:
            raise ModuleNotFoundError(f"Unable to find package '{pkg}'")
        return spec

    def _check_get_schematic_dirname(self, pkg_path: str) -> str:
        schematic_dirname = path.join(pkg_path, "schematics")
        if not path.isdir(schematic_dirname):
            raise ValueError(
                f"Unable to locate directory 'schematics/' in path {schematic_dirname}"
            )
        return schematic_dirname

    def _check_get_schematic_path(self, schematic_dirname: str, schematic: str) -> str:

        schematic_path = path.join(schematic_dirname, schematic)
        if not path.isdir(schematic_path):
            raise ValueError(
                f"Unable to locate schematic '{schematic}' in path {schematic_path}"
            )
        return schematic_path

    def _check_get_schematic(self, schematic: str, spec: importli.ModuleSpec) -> None:

        pkg_path: str = path.dirname(spec.origin)
        schematic_dirname = self._check_get_schematic_dirname(pkg_path)
        schematic_path = self._check_get_schematic_path(schematic_dirname, schematic)

    def _check_render_schematic(
        self, pkg_schematic: str, args: List[Any], delim: str = ":"
    ):
        from os import path

        from flaskerize import generate

        pkg, schematic = self._split_pkg_schematic(pkg_schematic, delim=delim)
        spec = self._check_validate_package(pkg)
        self._check_get_schematic(schematic, spec)

        generate.a[schematic](args)

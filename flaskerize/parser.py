import os
from os import path
import argparse
import sys
from typing import Any, Dict, List, Tuple, Optional
from importlib.machinery import ModuleSpec


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


class FzArgumentParser(argparse.ArgumentParser):
    """Flaskerize argument parser with default common options"""

    def __init__(
        self,
        schema: Optional[str] = None,
        xtra_schema_files: Optional[List[str]] = None,
    ):
        import json

        super().__init__()
        cfgs: List[Dict] = []
        # TODO: consolidate schema and xtra_schema_files
        if schema:
            cfgs.append(_load_schema(schema))
        if xtra_schema_files:
            cfgs.extend([_load_schema(file) for file in xtra_schema_files])

        for cfg in cfgs:
            for option in cfg["options"]:
                switches = [option.pop("arg")] + option.pop("aliases", [])
                self.add_argument(*switches, **option)


class Flaskerize(object):
    def __init__(self, args):
        import os

        print("\n\n\n ARGS = ", args)
        dirname = os.path.dirname(__file__)
        parser = FzArgumentParser(
            os.path.join(os.path.dirname(__file__), "global/schema.json")
        )
        parsed = parser.parse_args(args[1:2])
        getattr(self, parsed.command[0])(args[2:])

    def attach(self, args):
        from flaskerize.attach import attach

        arg_parser = FzArgumentParser()
        arg_parser.add_argument(
            "--to",
            type=str,
            required=True,
            help="Flask app factory function to attach blueprint",
        )
        arg_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Dry run -- don't actually create any files.",
        )
        arg_parser.add_argument("bp", type=str, help="Blueprint to attach")
        parse = arg_parser.parse_args(args)
        attach(parse)

    def bundle(self, args):
        """
        Generate a new Blueprint from a source static site and attach it
        to an existing Flask application
        """
        import os

        from flaskerize import generate

        DEFAULT_BP_NAME = "_fz_bp.py"
        DEFAULT_WSGI_NAME = "wsgi.py"
        DEFAULT_GUNICORN_ENTRY = f"{DEFAULT_WSGI_NAME.replace('.py', '')}:app"

        arg_parser = FzArgumentParser()
        arg_parser.add_argument(
            "output_name",
            type=str,
            default=None,
            help="Base name for outputted resource",
        )

        arg_parser.add_argument(
            "--output-file", "-o", type=str, help="Name of output file"
        )

        arg_parser.add_argument(
            "--source", "--from", type=str, help="Path of input static site to bundle"
        )

        arg_parser.add_argument(
            "--to",
            type=str,
            required=True,
            help="Flask app factory function to attach blueprint",
        )

        arg_parser.add_argument(
            "--with-wsgi",
            action="store_true",
            help="Also generate a wsgi.py for gunicorn",
        )

        arg_parser.add_argument(
            "--with-dockerfile", action="store_true", help="Also generate a Dockerfile"
        )

        arg_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Dry run -- don't actually create any files.",
        )

        parsed = arg_parser.parse_args(args + [DEFAULT_BP_NAME])

        if parsed.source and not parsed.source.endswith("/"):
            print(
                f"Input source {parsed.source} does not end with trailing /, adding "
                "for you"
            )
            parsed.source += "/"

        generate.a["blueprint"](parsed)

        if not parsed.dry_run:
            self.attach(f"--to {parsed.to} {DEFAULT_BP_NAME}".split())

    def generate(self, args):
        import os

        arg_parser = FzArgumentParser(
            schema=os.path.join(os.path.dirname(__file__), "global/generate.json")
        )
        parsed, rest = arg_parser.parse_known_args(args)
        print(f"parsed = {parsed}")
        schematic = parsed.schematic
        root_name = parsed.name
        dry_run = parsed.dry_run
        root, name = path.split(root_name)

        # TODO: cleanup logic for when full schematic path is passed versus providing a
        # package name. Perhaps just use the same param but check if it is pathlike and
        # assume package-like if it doesn't exist
        if parsed.schematic_path:
            self._check_render_schematic(
                schematic,
                name=name,
                root=root,
                dry_run=dry_run,
                full_schematic_path=parsed.schematic_path,
                args=rest,
            )
        else:
            self._check_render_schematic(
                schematic, root=root, name=name, dry_run=dry_run, args=rest
            )

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

    def _check_validate_package(self, pkg: str) -> ModuleSpec:
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

    def _check_get_schematic(self, schematic: str, spec: ModuleSpec) -> str:

        pkg_path: str = path.dirname(spec.origin)
        schematic_dirname = self._check_get_schematic_dirname(pkg_path)
        schematic_path = self._check_get_schematic_path(schematic_dirname, schematic)
        return schematic_path

    def _check_render_schematic(
        self,
        pkg_schematic: str,
        root: str,
        name: str,
        args: List[Any],
        full_schematic_path: Optional[str] = None,
        dry_run: bool = False,
        delim: str = ":",
    ) -> None:
        from os import path

        from flaskerize import generate

        if full_schematic_path is not None:
            schematic_path = full_schematic_path
        else:
            pkg, schematic = self._split_pkg_schematic(pkg_schematic, delim=delim)
            module_spec = self._check_validate_package(pkg)
            schematic_path = self._check_get_schematic(schematic, module_spec)
        self.render_schematic(
            schematic_path, root=root, name=name, dry_run=dry_run, args=args
        )

    def render_schematic(
        self,
        schematic_path: str,
        root: str,
        name: str,
        args: List[Any],
        dry_run: bool = False,
    ) -> None:
        from flaskerize.render import SchematicRenderer

        SchematicRenderer(schematic_path, root=root, dry_run=dry_run).render(name, args)


from os import path, makedirs
import argparse
from typing import Any, Dict, List, Optional

from flaskerize.parser import FzArgumentParser


class SchematicRenderer:
    """Render Flaskerize schematics"""

    def __init__(self, schematic_path: str, root: str = "./"):
        from jinja2 import Environment

        self.schematic_path = schematic_path
        self.root = root
        self.arg_parser = self._check_get_arg_parser()
        self.env = Environment()

    def _check_get_arg_parser(self) -> Optional[argparse.ArgumentParser]:
        """Load argument parser from schema.json, if provided"""

        import json

        schema_path = f"{self.schematic_path}/schema.json"
        if not path.isfile(schema_path):
            return None
        return FzArgumentParser(schema=schema_path)

    def _get_template_files(self) -> List[str]:
        from pathlib import Path

        return [str(p) for p in Path(self.schematic_path).glob("**/*.template*")]

    def _generate_outfile(self, template_file: str, root: str):
        full_path = path.join(root, path.relpath(template_file, self.schematic_path))
        without_template = "".join(full_path.rsplit(".template"))
        return without_template

    def render_from_file(self, template_file: str, context: Dict) -> None:
        outfile = self._generate_outfile(template_file, self.root)
        outdir = path.dirname(outfile)
        with open(template_file, "r") as fid:
            if not path.exists(outdir):
                makedirs(outdir)
            with open(outfile, "w") as fout:
                tpl = self.env.from_string(fid.read())
                fout.write(tpl.render(**context))

    def render(self, name: str, args: List[Any]) -> None:
        """Renders the schematic"""

        print(f"schematic_path = {self.schematic_path}")
        print(f"args = {args}")

        if self.arg_parser is None:
            context: Dict = {"name": name}
        else:
            context = vars(self.arg_parser.parse_args(args))
            if "name" in context:
                raise ValueError(
                    "Collision between Flaskerize-reserved parameter 'name' and "
                    "parameter found in schema.json corresponding to "
                    f"{self.schematic_path}"
                )
            context = {**context, "name": name}
        template_files = self._get_template_files()

        for filename in template_files:
            self.render_from_file(filename, context=context)
        print(f"template_files = {template_files}")
        # if not template_files:
        # raise ValueError(f"No template files found in {self.schematic_path}")

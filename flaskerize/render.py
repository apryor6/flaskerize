from os import path, makedirs
import argparse
from typing import Any, Dict, List, Optional
from termcolor import colored

from flaskerize.parser import FzArgumentParser


class SchematicRenderer:
    """Render Flaskerize schematics"""

    def __init__(self, schematic_path: str, root: str = "./", dry_run: bool = False):
        from jinja2 import Environment

        self.schematic_path = schematic_path
        self.root = root
        self.arg_parser = self._check_get_arg_parser()
        self.env = Environment()
        self.dry_run = dry_run
        self._directories_created: List[str] = []
        self._files_created: List[str] = []
        self._files_delete: List[str] = []
        self._files_modified: List[str] = []

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
        outdir = path.dirname(outfile) or "."

        # TODO: Refactor dry-run and file system interactions to a composable object
        # passed into this class rather than it containing the write logic
        with open(template_file, "r") as fid:
            tpl = self.env.from_string(fid.read())

            # Update status of creation, modification, etc
            # TODO: This behavior does not belong in this method or this class at that
            if path.exists(outfile):
                self._files_modified.append(outfile)
            else:
                self._files_created.append(outfile)
            if not path.exists(outdir):
                makedirs(outdir)
                self._directories_created.append(outdir)

            if not self.dry_run:
                if not path.exists(outdir):
                    makedirs(outdir)
                with open(outfile, "w") as fout:
                    fout.write(tpl.render(**context))
            else:
                print(tpl.render(**context))

    def print_summary(self):
        """Print summary of operations performed"""

        print(
            f"""
Flaskerize job summary:

        Schematic generation successful!
        Full schematic path {self.schematic_path}

        {len(self._directories_created)} directories created
        {len(self._files_created)} files created
        {len(self._files_delete)} files deleted
        {len(self._files_modified)} files modified
        """
        )
        for dirname in self._directories_created:
            self._print_created(dirname)
        for filename in self._files_created:
            self._print_created(filename)
        for filename in self._files_delete:
            self._print_deleted(filename)
        for filename in self._files_modified:
            self._print_modified(filename)

    def _print_modified(self, value: str) -> None:

        COLOR = "blue"
        BASE = "MODIFIED"
        print(f"{colored(BASE, COLOR)}: {value}")

    def _print_deleted(self, value: str) -> None:

        COLOR = "red"
        BASE = "DELETED"
        print(f"{colored(BASE, COLOR)}: {value}")

    def _print_created(self, value: str) -> None:

        COLOR = "green"
        BASE = "CREATED"
        print(f"{colored(BASE, COLOR)}: {value}")

    def render(self, name: str, args: List[Any]) -> None:
        """Renders the schematic"""

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
        self.print_summary()
        # if not template_files:
        # raise ValueError(f"No template files found in {self.schematic_path}")

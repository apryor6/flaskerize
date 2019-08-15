from os import path, makedirs
import argparse
from typing import Any, Callable, Dict, List, Optional
from termcolor import colored

from flaskerize.parser import FzArgumentParser


class SchematicRenderer:
    """Render Flaskerize schematics"""

    def __init__(self, schematic_path: str, root: str = "./", dry_run: bool = False):
        from jinja2 import Environment

        self.schematic_path = schematic_path
        self.root = root

        self.schema_path = self._get_schema_path()
        self._load_schema()

        self.arg_parser = self._check_get_arg_parser()
        self.env = Environment()
        self.dry_run = dry_run
        self._directories_created: List[str] = []
        self._files_created: List[str] = []
        self._files_deleted: List[str] = []
        self._files_modified: List[str] = []

    def _load_schema(self) -> None:
        if self.schema_path:
            import json

            with open(self.schema_path, "r") as fid:
                self.config = json.load(fid)
        else:
            self.config = {}

    def _get_schema_path(self) -> Optional[str]:

        schema_path = path.join(self.schematic_path, "schema.json")
        if not path.isfile(schema_path):
            return None
        return schema_path

    def _check_get_arg_parser(
        self, schema_path: Optional[str] = None
    ) -> FzArgumentParser:
        """Load argument parser from schema.json, if provided"""

        return FzArgumentParser(schema=schema_path or self.schema_path)

    def get_template_files(self) -> List[str]:
        from pathlib import Path

        filenames = []
        patterns = self.config.get("templateFilePatterns", [])
        for pattern in patterns:
            filenames.extend([str(p) for p in Path(self.schematic_path).glob(pattern)])
        ignore_filenames = self._get_ignore_files()
        filenames = list(set(filenames) - set(ignore_filenames))
        return filenames

    def _get_ignore_files(self) -> List[str]:
        from pathlib import Path

        ignore_filenames = []
        ignore_patterns = self.config.get("ignoreFilePatterns", [])
        for pattern in ignore_patterns:
            ignore_filenames.extend(
                [str(p) for p in Path(self.schematic_path).glob(pattern)]
            )
        return ignore_filenames

    def _generate_outfile(
        self, template_file: str, root: str, context: Optional[Dict] = None
    ) -> str:
        full_path = path.join(root, path.relpath(template_file, self.schematic_path))
        outfile_name = "".join(full_path.rsplit(".template"))
        tpl = self.env.from_string(outfile_name)
        if context is None:
            context = {}
        return tpl.render(**context)

    def render_from_file(self, template_file: str, context: Dict) -> None:
        outfile = self._generate_outfile(template_file, self.root, context=context)
        outdir = path.dirname(outfile) or "."
        print("outdir = ", outdir)
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
        {len(self._files_deleted)} files deleted
        {len(self._files_modified)} files modified
        """
        )
        for dirname in self._directories_created:
            self._print_created(dirname)
        for filename in self._files_created:
            self._print_created(filename)
        for filename in self._files_deleted:
            self._print_deleted(filename)
        for filename in self._files_modified:
            self._print_modified(filename)

    def _print_created(self, value: str) -> None:

        COLOR = "green"
        BASE = "CREATED"
        print(f"{colored(BASE, COLOR)}: {value}")

    def _print_modified(self, value: str) -> None:

        COLOR = "blue"
        BASE = "MODIFIED"
        print(f"{colored(BASE, COLOR)}: {value}")

    def _print_deleted(self, value: str) -> None:

        COLOR = "red"
        BASE = "DELETED"
        print(f"{colored(BASE, COLOR)}: {value}")

    def _load_run_function(self, run_function_path: str) -> Callable:
        from importlib.util import spec_from_file_location, module_from_spec

        spec = spec_from_file_location("run", run_function_path)

        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "run"):
            raise ValueError(f"No method 'run' function found in {run_function_path}")
        return getattr(module, "run")

    def render(self, name: str, args: List[Any]) -> None:
        """Renders the schematic"""

        context = vars(self.arg_parser.parse_args(args))
        if "name" in context:
            raise ValueError(
                "Collision between Flaskerize-reserved parameter "
                "'name' and parameter found in schema.json corresponding "
                f"to {self.schematic_path}"
            )
        context = {**context, "name": name}

        try:
            run = self._load_run_function(
                run_function_path=path.join(self.schematic_path, "run.py")
            )
        except (ImportError, ValueError, FileNotFoundError) as e:
            run = default_run
        run(renderer=self, context=context)


def default_run(renderer: SchematicRenderer, context: Dict[str, Any]) -> None:
    """Default run method"""

    template_files = renderer.get_template_files()

    for filename in template_files:
        renderer.render_from_file(filename, context=context)
    renderer.print_summary()

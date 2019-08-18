v0.1.9

- Change attachment line so choice of quotation does not conflict

v0.2.0

- Enable Flask() calls with existing static directories and dramatically simplify handling of static files from blueprints

v0.3.0

- Substantial refactor to use Jinja templates for rendering
- Enable configurable schema.json for custom parameters from schematic author
- Enable multi-glob parameters in schema.json for determining file patterns to include, ignore, render, etc
- Dramatically increase test coverage
- Provide hook for user-provided run method

v0.4.0

- Implement run.py as a hook for custom run functionality
- Implement custom_functions.py for enabling custom template functions within schematic scope

v0.5.0

- Add setup schematic and tests
- Create README for available schematics

v0.6.0

- Implement entity schematic
- Improve logic for creation of templated directories vs files

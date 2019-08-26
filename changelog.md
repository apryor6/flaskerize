0.1.9

- Change attachment line so choice of quotation does not conflict

0.2.0

- Enable Flask() calls with existing static directories and dramatically simplify handling of static files from blueprints

0.3.0

- Substantial refactor to use Jinja templates for rendering
- Enable configurable schema.json for custom parameters from schematic author
- Enable multi-glob parameters in schema.json for determining file patterns to include, ignore, render, etc
- Dramatically increase test coverage
- Provide hook for user-provided run method

0.4.0

- Implement run.py as a hook for custom run functionality
- Implement custom_functions.py for enabling custom template functions within schematic scope

0.5.0

- Add setup schematic and tests
- Create README for available schematics

0.6.0

- Implement entity schematic
- Improve logic for creation of templated directories vs files

0.6.0

- Implement schematic schematic

0.8.0

- Implement a schematic for creating basic plotly + Flask application

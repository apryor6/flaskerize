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

0.8.1

- Remove a file

0.9.0

- Substantially refactor internal file manipulation mechanism to use a staging, in-memory filesystem. See [here](https://github.com/apryor6/flaskerize/pull/31) for more discussion

0.10.0

- Internal refactor to use PyFilesystem with a two-step staging of file changes and modifications using an in-memory buffer followed by a commit step upon success at which time the changes are actually made to the file system, unless on a dry run

0.11.0

- Allow user to provide full path to schematics directory or the root level above it, such as for a library

0.12.0

- Add the `flask-api` schematic for easy creation of a new Flask API project w/ SQL Alchemy that follows the pattern described [here](http://alanpryorjr.com/2019-05-20-flask-api-example/)

0.14.0

- Update from Flask-RESTplus to flask-restx

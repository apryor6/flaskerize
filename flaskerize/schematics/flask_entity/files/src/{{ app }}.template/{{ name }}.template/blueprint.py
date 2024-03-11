from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from .model import {{ capitalize(name) }}

blueprint = Blueprint('{{ name }}', __name__,
                      url_prefix="/{{ name }}",
                      template_folder='templates',
                      static_folder='{{ name }}_static')


@blueprint.route('/', defaults={'page': '{{ name }}'})
@blueprint.route('/<page>')
def {{ name }}(page):
    {{ name }}_list = {{ capitalize(name) }}.query.all()
    try:
        return render_template(f'{page}.html', title="{{ capitalize(name) }}", {{ name }}_list={{ name }}_list)
    except TemplateNotFound:
        abort(404)

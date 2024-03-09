from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

blueprint = Blueprint('status', __name__,
                      url_prefix='/status',
                      template_folder='templates',
                      static_folder='status_static')


@blueprint.route('/', defaults={'page': 'status'})
@blueprint.route('/<page>')
def status(page):
    try:
        return render_template(f'{page}.html', title="Status")
    except TemplateNotFound:
        abort(404)

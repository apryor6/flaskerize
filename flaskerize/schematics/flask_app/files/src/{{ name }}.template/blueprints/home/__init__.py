from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

blueprint = Blueprint('home', __name__,
                      url_prefix='/',
                      template_folder='templates',
                      static_folder='home_static')


@blueprint.route('/', defaults={'page': 'home'})
@blueprint.route('/<page>')
def show(page):
    try:
        return render_template(f'{page}.html', title="Home")
    except TemplateNotFound:
        abort(404)

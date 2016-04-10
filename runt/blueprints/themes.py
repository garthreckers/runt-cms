import config
from runt.controllers import *
from flask import Blueprint
from ..models import Settings


_theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value

template_folder = config.ROOT_DIR + '/themes/' + _theme
static_folder = template_folder + '/static'

themes = Blueprint('themes', __name__,
					template_folder=template_folder,
					static_folder=static_folder)

"""
Themes Stuff
"""
t = ThemeController()

@themes.app_template_global('field_value')
def field_value(id, field_id):
	return t.get_field(id, field_id)


@themes.route('/')
def theme_index():
	return t.index()

@themes.route('/<slug>', strict_slashes=False)
def theme_pages(slug):
	return t.pages(slug)

@themes.route('/<obj>/<slug>', strict_slashes=False)
def theme_object_pages(obj, slug):
	return t.object_pages(obj, slug)

@themes.context_processor
def theme_global_vars():	
	return t.global_variables() or {}
import config
from runt.controllers import *
from flask import Blueprint
from runt.models import Settings

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

@themes.route('/')
def theme_index():
	return t.index()

@themes.route('/<slug>', strict_slashes=False)
def theme_pages(slug):
	return t.pages(slug)

@themes.route('/<obj>/<slug>', strict_slashes=False)
def theme_object_pages(obj, slug):
	return t.object_pages(obj, slug)
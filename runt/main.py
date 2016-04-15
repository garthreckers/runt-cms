"""
Builds the routes, theme loader,
and other basics for Runt CMS
"""
import os
import json
from collections import OrderedDict
from datetime import timedelta
import config
from flask import Flask, send_from_directory, redirect,\
					url_for
from .models import *
from .utilities.extensions import inject_footer, inject_header
from .admin.install import runt_installed
from . import blueprints
from .utilities.images import Images

runt = Flask(__name__, static_url_path='/overriding-static')

runt.register_blueprint(blueprints.extensions)
runt.register_blueprint(blueprints.themes)
runt.register_blueprint(blueprints.admin, url_prefix='/admin')

imgs = Images()
def get_image_size(url, size):
	return imgs.get_image(url, size)

runt.jinja_env.globals.update(get_image_size=get_image_size)


@runt.context_processor
def ext_inject_footer():
	"""
	injects into the footer of the template
	ie. javascript
	"""
	return inject_footer()

@runt.context_processor
def ext_inject_header():
	"""
	injects into the header of the template
	ie. javascript, stylesheets, SEO tags, etc
	"""
	return inject_header()


@runt.context_processor
def admin_menu():
	"""
	Build the admin menu dictionary that is passed
	to the admin templates
	"""
	menu = OrderedDict()
	menu["Admin"] = "/admin"
	menu["Pages"] = "/admin/pages?object-type=page"

	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	objects_json = config.ROOT_DIR + '/themes/' + theme + '/objects.json'

	if os.path.exists(objects_json):
		with open(objects_json, "r") as _oj:
			object_data = json.loads(_oj.read())

			for _ob, _o_dict in object_data.items():
				display = _o_dict['display']
				menu[display] = "/admin/pages?object-type=" + _ob

	menu["Theme"] = "/admin/theme"
	menu["Extensions"] = "/admin/extensions"
	menu["Users"] = "/admin/users"
	menu["Settings"] = "/admin/settings"

	return dict(admin_menu=menu)

@runt.route('/uploads/<path:filename>')
def uploads_static_folder(filename):
	static_path = config.ROOT_DIR + '/uploads/'
	return send_from_directory(static_path, filename)

runt.secret_key = os.urandom(24)
runt.permanent_session_lifetime = timedelta(hours=3)

if not config.PRODUCTION:
	runt.debug = True

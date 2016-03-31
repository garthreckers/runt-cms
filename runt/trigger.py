"""
Builds the routes, theme loader,
and other basics for Runt CMS
"""
import os
import json
from collections import OrderedDict
from datetime import timedelta
import config
from flask import Flask, send_from_directory
from .models import Settings
from .extensions import inject_footer, inject_header
from . import blueprints

TRIGGER = Flask(__name__, static_url_path='/overriding-static')

TRIGGER.register_blueprint(blueprints.extensions)
TRIGGER.register_blueprint(blueprints.themes)
TRIGGER.register_blueprint(blueprints.admin, url_prefix='/admin')


@TRIGGER.context_processor
def ext_inject_footer():
	"""
	injects into the footer of the template
	ie. scripts
	"""
	return inject_footer()

@TRIGGER.context_processor
def ext_inject_header():
	"""
	injects into the header of the template
	ie. scripts, stylesheets, SEO tags, etc
	"""
	return inject_header()


@TRIGGER.context_processor
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
	menu["Users"] = "/admin/users"

	return dict(admin_menu=menu)

@TRIGGER.route('/uploads/<path:filename>')
def uploads_static_folder(filename):
	static_path = config.ROOT_DIR + '/uploads/'
	return send_from_directory(static_path, filename)

TRIGGER.secret_key = os.urandom(24)
TRIGGER.permanent_session_lifetime = timedelta(hours=3)

TRIGGER.debug = True

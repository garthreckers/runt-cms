"""
Builds the routes, theme loader,
and other basics for Runt CMS
"""
import os
import compileall
import jinja2
import json
import sys
import config
from .extensions import load_template, inject_footer, inject_header
from peewee import *
from collections import OrderedDict
from datetime import timedelta
from functools import wraps
from flask import Flask, render_template, request,\
	send_from_directory, redirect, url_for
from .admin.install import check_install
from .admin.auth import auth, check_username, logged_in, login_checker
from .models import *
from runt import blueprints


""" 
Assign Flask and set static_url_path to
a random directory so that /static/ can 
be used later.
"""
trigger = Flask(__name__, static_url_path='/runt-static-override')

trigger.register_blueprint(blueprints.extensions)
trigger.register_blueprint(blueprints.themes)
trigger.register_blueprint(blueprints.admin, url_prefix='/admin')


@trigger.context_processor
def ext_inject_footer():
	return inject_footer()

@trigger.context_processor
def ext_inject_header():
	return inject_header()


@trigger.context_processor
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
		with open(objects_json, "r") as oj:
			object_data = json.loads(oj.read())
				
			for o, o_dict in object_data.items():
				display = o_dict['display']
				menu[display] = "/admin/pages?object-type=" + o

	menu["Theme"] = "/admin/theme"
	menu["Users"] = "/admin/users"

	return dict(admin_menu=menu)

"""
Set up some session defaults
"""
trigger.secret_key = os.urandom(24)
trigger.permanent_session_lifetime = timedelta(hours=3)

trigger.debug = True

"""
Change default directors for Jinja2 Templates
""
theme_loader = jinja2.ChoiceLoader([
		trigger.jinja_loader,	
		jinja2.FileSystemLoader([
				'themes',
				'runt/admin/templates'
			])
	])
trigger.jinja_loader = theme_loader
"""



@trigger.route('/uploads/<path:filename>')
def uploads_static_folder(filename):
	static_path = config.ROOT_DIR + '/uploads/'
	return send_from_directory(static_path, filename)


"""
General Admin Views
"""

#@trigger.route('/install', methods=['GET', 'POST'], strict_slashes=False)
#def install_runt():
#	return admin.install()

"""
Users
"""







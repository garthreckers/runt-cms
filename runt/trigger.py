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
from .controllers import users, admin, settings, theme, pages

""" 
Assign Flask and set static_url_path to
a random directory so that /static/ can 
be used later.
"""
trigger = Flask(__name__, static_url_path='/runt-static-override')

"""
Set up some session defaults
"""
trigger.secret_key = os.urandom(24)
trigger.permanent_session_lifetime = timedelta(hours=3)

trigger.debug = True

"""
Change default directors for Jinja2 Templates
"""
theme_loader = jinja2.ChoiceLoader([
		trigger.jinja_loader,	
		jinja2.FileSystemLoader([
				'themes',
				'runt/admin/templates'
			])
	])
trigger.jinja_loader = theme_loader


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

"""extensions"""

@trigger.context_processor
def ext_inject_footer():
	return inject_footer()

@trigger.context_processor
def ext_inject_header():
	return inject_header()

@trigger.route('/<ext>/static/<path:filename>')
def ext_static_files(ext, filename):
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	static_path = config.ROOT_DIR + '/extensions/' + ext + '/static'
	return send_from_directory(static_path, filename)


@trigger.route('/uploads/<path:filename>')
def uploads_static_folder(filename):
	static_path = config.ROOT_DIR + '/uploads/'
	return send_from_directory(static_path, filename)


"""
Set up static admin css folder
"""

@trigger.route('/admin/static/<path:filename>', strict_slashes=False)
def admin_static(filename):
	"""
	This sets up a static folder for the admin templating
	"""
	runt_root = os.path.dirname(os.path.realpath(__file__))
	return send_from_directory(runt_root + '/admin/templates/', filename)


"""
General Admin Views
"""
@trigger.route('/admin', strict_slashes=False)
def admin_index():
	return admin.index()

@trigger.route('/admin/login', methods=['GET', 'POST'], strict_slashes=False)
def admin_login():
	return admin.login()

@trigger.route('/install', methods=['GET', 'POST'], strict_slashes=False)
def install_runt():
	return admin.install()

"""
Users
"""
@trigger.route('/admin/users', strict_slashes=False)
def admin_users_page():
	return users.index()

@trigger.route("/admin/users/add/", methods=['GET', 'POST'], strict_slashes=False)
def admin_users_add():
	return users.add()

@trigger.route("/admin/users/delete/<uname>", methods=['GET', 'POST'], strict_slashes=False)
def admin_users_delete(uname):
	return users.delete(uname)

"""
Settings
"""
@trigger.route("/admin/theme", methods=['GET', 'POST'], strict_slashes=False)
def admin_theme():
	return settings.themes()

"""
Extensions
"""
@trigger.route("/admin/extensions", methods=['GET', 'POST'], strict_slashes=False)
def admin_extensions():

	if request.method == 'POST':
		name = request.form['ext_name']
		activation = True if request.form['activation'] == 'activate' else False

		select_ext = Extensions.select().where(Extensions.name == name)

		if select_ext.exists():
			Extensions.update(active=activation).where(Extensions.name == name).execute()
		else:
			Extensions.create(name=name, active=activation)

		return redirect(url_for('admin_install_extensions'))

		
	exts = Extensions.select().order_by(+Extensions.name)


	exts_dict = {}
	for e in exts:
		_exts_temp_dict = {}
		_e_path = config.ROOT_DIR + "/extensions/" + e.name + "/extension.json"
		if os.path.exists(_e_path):
			with open(_e_path, "r") as f:
				_exts_json = json.loads(f.read())['extension_details']
				_exts_temp_dict.update(_exts_json)

		if e.active == True:
			_exts_temp_dict.update({"active": True})
			exts_dict.update({e.name: _exts_temp_dict})
		else:
			_exts_temp_dict.update({"active": False})
			exts_dict.update({e.name: _exts_temp_dict})

	return render_template("admin-extensions.html", pageheader="Extensions", extensions=exts_dict)

"""
Basically when admin/extensions/install is hit, the iframe will fail but will successfully
restart the python server. 
"""
@trigger.route("/admin/extensions/install")
def admin_install_extensions():
	return render_template("admin-extensions-install.html", pageheader="Processing...")

@trigger.route("/admin/restart_app")
def admin_restart_app():
	python = sys.executable
	os.execl(python, python, * sys.argv)


"""
Pages
"""
@trigger.route("/admin/pages", strict_slashes=False)
def admin_pages():
	return pages.all()

@trigger.route("/admin/pages/add", methods=['GET', 'POST'], strict_slashes=False)
def admin_add_pages():
	return pages.add()

@trigger.route("/admin/pages/edit/<id>", methods=['GET', 'POST'], strict_slashes=False)
def admin_edit_pages(id):
	return pages.edit(id)


"""
Theme Stuff
"""

@trigger.route('/static/<path:filename>')
def theme_path_static(filename):
	return theme.static(filename)

@trigger.route('/')
def theme_index():
	return theme.index()

@trigger.route('/<slug>', strict_slashes=False)
def theme_pages(slug):
	return theme.pages(slug)

@trigger.route('/<obj>/<slug>', strict_slashes=False)
def theme_object_pages(obj, slug):
	return theme.object_pages(obj, slug)
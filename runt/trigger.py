"""

Builds the basics for Runt

"""
import os
import jinja2
import json
from pprint import *
from peewee import *
from datetime import timedelta
from functools import wraps
from . import config
from flask import Flask, render_template, request,\
	send_from_directory, redirect, url_for
from .admin.install import check_install
from .admin.auth import auth, check_username, logged_in
from .models.users_model import Users
from .models.base_model import BaseModel
from .models.settings_model import Settings
from .models.page_model import Page
from .controllers import users, admin, settings

trigger = Flask(__name__)
trigger.secret_key = os.urandom(24)
trigger.permanent_session_lifetime = timedelta(hours=3)

trigger.debug = True

theme_loader = jinja2.ChoiceLoader([
		trigger.jinja_loader,	
		jinja2.FileSystemLoader([
				'runt/themes',
				'runt/admin/templates'
			])
	])
trigger.jinja_loader = theme_loader

"""
Set up static admin css folder
"""
@trigger.route('/admin/static/<path:filename>', strict_slashes=False)
def admin_static(filename):
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
Pages
"""
@trigger.route("/admin/page", strict_slashes=False)
def admin_pages():
	pages = Page.select().where(Page.object_type == 'page').order_by(+Page.title)
	return render_template("admin-all-pages.html", pages=pages)



"""
Theme Stuff
"""

"""
Need to figure out how to get this to work
@trigger.route('/static/<path:path>')
def theme_w_path_static(path):
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	static_path = RUNT_ROOT + '/themes/' + theme + '/static/'
	print(static_path)
	return send_from_directory(static_path, path)"""

@trigger.route('/static/<filename>', strict_slashes=False)
def theme_static(filename):
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	runt_root = os.path.dirname(os.path.realpath(__file__))
	static_path = runt_root + '/themes/' + theme + '/static/'
	print(static_path)
	return send_from_directory(static_path, filename)

@trigger.route('/')
def index():
	content = {}
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	template_json = config.RUNT_ROOT + '/themes/' + theme + '/index.json'
	if os.path.exists(template_json):
		with open(template_json, "r") as tj:
			_t_decode = json.loads(tj.read())
			for i, t in _t_decode.items():
				_p_obj = Page.select().where(Page.object_type == t).order_by(-Page.id)
				content[t] = _p_obj

	template_name = theme + '/index.html'
	return render_template(template_name, content=content)

@trigger.route('/<id>')
def page(id):
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	content = Page.select().where(Page.id == id).get()
	template_name = theme + '/page.html'
	return render_template(template_name, content=content)

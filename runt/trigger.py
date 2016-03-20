"""

Builds the basics for Runt

"""
import os
import jinja2
from pprint import *
from peewee import *
from datetime import timedelta
from functools import wraps
from . import config
from flask import Flask, render_template, request,\
	send_from_directory, redirect, url_for
from .admin.install import install, check_install
from .admin.auth import auth, check_username, logged_in
from .models.users_model import Users
from .models.base_model import BaseModel
from .models.settings_model import Settings
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
Homepage
"""
@trigger.route('/')
def index():
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	template_name = theme + '/index.html'
	return render_template(template_name)

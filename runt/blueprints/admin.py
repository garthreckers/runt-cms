import os, json
import config
from collections import OrderedDict
from flask import Blueprint
from runt.controllers import *
from runt.models.settings_model import Settings

admin_static = config.RUNT_ROOT + '/admin/templates/'

admin = Blueprint('admin', __name__,
						template_folder='../admin/templates',
						static_folder=admin_static)

a = AdminController()
p = PageController()
s = SettingsController()
u = UserController()

"""
Set up static admin css folder
"""
#@admin.route('/admin/static/<path:filename>', strict_slashes=False)
#def admin_static(filename):
"""
This sets up a static folder for the admin templating
"""
#runt_root = os.path.dirname(os.path.realpath(__file__))
#return send_from_directory(, filename)


"""
Basic Admin Views
"""
@admin.route('/', strict_slashes=False)
def admin_index():
	return a.index()

@admin.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def admin_login():
	return a.login()


"""
Users
"""
@admin.route('/users', strict_slashes=False)
def admin_users_page():
	return u.index()

@admin.route("/users/add/", methods=['GET', 'POST'], strict_slashes=False)
def admin_users_add():
	return u.add()

@admin.route("/users/delete/<uname>", methods=['GET', 'POST'], strict_slashes=False)
def admin_users_delete(uname):
	return u.delete(uname)


"""
Settings
"""
@admin.route("/theme", methods=['GET', 'POST'], strict_slashes=False)
def admin_theme():
	return s.themes()



"""
Pages
"""
@admin.route("/pages", strict_slashes=False)
def admin_pages():
	return p.all()

@admin.route("/pages/add", methods=['GET', 'POST'], strict_slashes=False)
def admin_add_pages():
	return p.add()

@admin.route("/pages/edit/<id>", methods=['GET', 'POST'], strict_slashes=False)
def admin_edit_pages(id):
	return p.edit(id)
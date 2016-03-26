"""
Builds the routes, theme loader,
and other basics for Runt CMS
"""
import os
import jinja2
import json
import config
from extensions import exts
from .extensions import load_template
from peewee import *
from collections import OrderedDict
from datetime import timedelta
from functools import wraps
from flask import Flask, render_template, request,\
	send_from_directory, redirect, url_for
from .admin.install import check_install
from .admin.auth import auth, check_username, logged_in
from .models.users_model import Users
from .models.base_model import BaseModel
from .models.settings_model import Settings
from .models.extensions_model import Extensions
from .models.pages_model import Pages
from .controllers import users, admin, settings

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
			print('**********************' + name)
			Extensions.update(active=activation).where(Extensions.name == name).execute()
		else:
			Extensions.create(name=name, active=activation)
		

	extensions = {}
	for e in exts:
		if Extensions.select().where((Extensions.name == e) & (Extensions.active == True)):
			extensions.update({e: True})
		else:
			extensions.update({e: False})

	return render_template("admin-extensions.html", pageheader="Extensions", extensions=extensions)

"""
Pages
"""
@trigger.route("/admin/pages", strict_slashes=False)
def admin_pages():

	object_type = request.args.get('object-type') or 'page'
	pageheader = object_type.title() + ' Pages' if object_type != 'page' else 'Pages'

	pages = Pages.select().where(Pages.object_type == object_type).order_by(+Pages.title)

	return render_template("admin-all-pages.html", pages=pages, object_type=object_type, pageheader=pageheader)

@trigger.route("/admin/pages/add", methods=['GET', 'POST'], strict_slashes=False)
def admin_add_pages():

	object_type = request.args.get('object-type') or 'page'

	err_return = {}
	if request.method == 'POST':
		if not request.form['title']:
			err_return['title'] = "Title is required"
		if not request.form['slug']:
			err_return['slug'] = "Slug is required"
		if not request.form['content']:
			err_return['content'] = "Content is required"
		if not err_return:
			p = Pages(title=request.form['title'], slug=request.form['slug'], \
				content=request.form['content'], object_type=object_type)
			p.save()
			return redirect(url_for('admin_edit_pages', id=p.id))
	return render_template("admin-add-page.html", error=err_return, object_type=object_type)

@trigger.route("/admin/pages/edit/<id>", methods=['GET', 'POST'], strict_slashes=False)
def admin_edit_pages(id):
	object_type = request.args.get('object-type') or 'page'

	err_return = {}
	p = Pages.select().where(Pages.id == id)
	if p.exists():
		values = p.get()

		if request.method == 'POST':
			if not request.form['title']:
				err_return['title'] = "Title is required"
			if not request.form['slug']:
				err_return['slug'] = "Slug is required"
			if not request.form['content']:
				err_return['content'] = "Content is required"
			if not err_return:
				p_update = Pages.update(title=request.form['title'], slug=request.form['slug'], \
					content=request.form['content']).where(Pages.id == id).execute()
				values = {}
				values['title'] = request.form['title']
				values['slug'] = request.form['slug']
				values['content'] = request.form['content']
				values['id'] = id

		return render_template("admin-edit-page.html", values=values, error=err_return, object_type=object_type)

	return '404 page'


"""
Theme Stuff
"""

@trigger.route('/static/<path:filename>')
def theme_path_static(filename):
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	static_path = config.ROOT_DIR + '/themes/' + theme + '/static'
	return send_from_directory(static_path, filename)

@trigger.route('/')
def index():
	content = {}
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	template_json = config.ROOT_DIR + '/themes/' + theme + '/index.json'

	if os.path.exists(template_json):
		with open(template_json, "r") as tj:
			_t_decode = json.loads(tj.read())
			for k, v in _t_decode['objects'].items():
				_p_obj = None
				if v == "*":
					_p_obj = (Pages
								.select()
								.where(Pages.object_type == k)
								.order_by(-Pages.id))

				if type(v) is dict:
					_objs = []
					for inner_k, inner_v in v.items():
						_objs.append(inner_v)

					_p_obj = (Pages
								.select(*[getattr(Pages, a) for a in _objs])
								.where(Pages.object_type == k)
								.order_by(-Pages.id))
				
				_p_content = []
				for _p_dict in _p_obj.dicts():
					_p_content.append(_p_dict)
				content[k] = _p_content

	template_name = theme + '/index.html'

	return load_template(template_name, content=content)

@trigger.route('/<slug>', strict_slashes=False)
def pages(slug):
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	content = Pages.select().where(Pages.slug == slug, Pages.object_type == 'page').get()
	template_name = theme + '/page.html'
	return render_template(template_name, content=content)

@trigger.route('/<obj>/<slug>', strict_slashes=False)
def object_pages(obj, slug):
	if obj == "page":
		return
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	content = Pages.select().where(Pages.slug == slug, Pages.object_type == obj).get()
	
	template_set = ['page-' + str(obj) + '.html', 'page.html']

	for tn in template_set:

		if os.path.exists(config.ROOT_DIR + '/themes/' + theme + '/' + tn):

			template_name = theme + '/' + tn
			return render_template(template_name, content=content)

	return '404'
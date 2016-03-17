"""

Builds the basics for Runt

"""
import os
import jinja2
import pprint
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
Check if user is logged in using @login_checker decorator
"""
def login_checker(func):
	@wraps(func)
	def func_wrap(*args, **kwargs):
		if logged_in():
			return func(*args, **kwargs)
		else:
			return redirect(url_for('admin_login'))
	return func_wrap

"""
Set up static admin css folder
"""
@trigger.route('/admin/static/<path:filename>', strict_slashes=False)
def admin_static(filename):
	runt_root = os.path.dirname(os.path.realpath(__file__))
	return send_from_directory(runt_root + '/admin/templates/', filename)


@trigger.route('/admin', strict_slashes=False)
def admin():
	if not logged_in():
		return redirect(url_for('admin_login'))
	return render_template('admin-main.html')
	

@trigger.route('/admin/login', methods=['GET', 'POST'], strict_slashes=False)
def admin_login():

	err_return = None
	if request.method == 'POST':
		if request.form['uname']:
			if check_username(request.form['uname']):
				if auth(username=request.form['uname'], password=request.form['password']):
					return redirect(url_for('admin'))
				
				err_return = "That username and password combination "
			else:
				err_return = "Username does not exist"
		else:
			err_return = "Username field is required"


	return render_template('admin-login.html', error=err_return)

@trigger.route('/admin/users', strict_slashes=False)
#@login_checker
def admin_users_page():
	return_list = Users.select(Users.id, Users.username, Users.level).order_by(Users.username)
	return render_template('admin-page.html', pageheader="Users", return_list=return_list)


@trigger.route("/admin/add/user", methods=['GET', 'POST'], strict_slashes=False)
def admin_user_add():

	err_return = {}
	values = {}

	if request.method == 'POST':
		u = Users()

		uname = request.form['uname']
		email = request.form['email']
		password = request.form['password']
		repeat_password = request.form['repeat-password']
		level = request.form['level']

		if not uname:
			err_return['err_uname'] = "Username field is required"
		elif u.select().where(Users.username == uname).exists():
			err_return['err_uname'] = "Username already exists"
		else:
			values['uname'] = uname

		if not email:
			err_return['err_email'] = "Email field is required"
		elif u.select().where(Users.email == email).exists():
			err_return['err_email'] = "Email already exists"
		else:
			values['email'] = email

		if not password:
			err_return['err_password'] = "Password field is required"

		if not repeat_password:
			err_return['err_password'] = "Both password fields are required"
		else:
			if password != repeat_password:
				err_return['err_password'] = "Passwords must match"


		if not err_return:
			p_word = u.hash_password(password)
			created = u.create(username=uname, password=p_word, email=email, level=level)
			if created: 
				return redirect(url_for('admin_users_page'))
			

	return render_template('admin-add-user.html', pageheader="Add User", error=err_return, values=values)

@trigger.route('/install', methods=['GET', 'POST'], strict_slashes=False)
def install_runt():
	if not check_install:
		return "You have already installed Runt CMS"

	err_return = {}
	values = {}
	if request.method == 'POST':

		"""
		Rework so things like username must begin 
		with a letter, password must be x long etc.
		"""
		if not request.form['uname']:
			err_return['err_uname'] = "Username field is required"
		else:
			values['uname'] = request.form['uname']

		if not request.form['email']:
			err_return['err_email'] = "Email field is required"
		else:
			values['email'] = request.form['email']

		if not request.form['password']:
			err_return['err_password'] = "Password field is required"

		if not request.form['repeat-password']:
			err_return['err_password'] = "Both password fields are required"
		else:
			if request.form['password'] != request.form['repeat-password']:
				err_return['err_password'] = "Passwords must match"

		if not err_return:
			install(username=request.form['uname'], email=request.form['email'], password=request.form['password'])
			return "<h1>Installed!</h1>"

	return render_template('admin-install.html', error=err_return, values=values)


	
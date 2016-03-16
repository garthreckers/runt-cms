"""

Builds the basics for Runt

"""
import os
import jinja2
from datetime import timedelta
from . import config
from flask import Flask, render_template, request,\
	send_from_directory, redirect, url_for
from .admin.install import install, check_install
from .admin.auth import auth, check_username, logged_in


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

@trigger.route("/admin")
def admin():
	if not logged_in():
		return redirect(url_for('admin_login'))
	return "logged in id: " + logged_in()
	

@trigger.route("/admin/login", methods=['GET', 'POST'])
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

"""
Set up static admin css folder
"""
@trigger.route('/admin/static/<path:filename>')
def admin_static(filename):
	runt_root = os.path.dirname(os.path.realpath(__file__))
	return send_from_directory(runt_root + '/admin/templates/', filename)


@trigger.route("/install", methods=['GET', 'POST'])
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


	
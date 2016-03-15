"""

Builds the basics for Runt

"""
import os
import jinja2
from datetime import timedelta
from . import config
from flask import Flask, render_template, request
from .utils.install import install, check_install
from .utils.auth import auth, check_username, logged_in


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


@trigger.route("/admin", methods=['GET', 'POST'])
def admin():

	err_return = None
	if request.method == 'POST':
		if request.form['uname']:
			if check_username(request.form['uname']):
				if auth(username=request.form['uname'], password=request.form['password']):
					return "<h1>BOOM LOGGED IN</h1>"
				
				err_return = "That username and password combination "
			else:
				err_return = "Username does not exist"
		else:
			err_return = "Username field is required"


	return render_template('admin-main.html', error=err_return)

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

@trigger.route("/admin/lockout")
def lockout_test():
	if logged_in():
		return "logged in id: " + logged_in()
	return "Not logged in... get out of here"

	
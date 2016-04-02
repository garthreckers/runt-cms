from ..admin.auth import login_checker
from runt.utils import noindex
from ..admin.install import runt_installed, install_runt
from flask import render_template, request

class AdminController():
	def __init__(self):
		pass

	#@login_checker
	@noindex
	def index(self):
		return render_template('admin-main.html')

	@noindex
	def login(self):
		"""
		Returns the login form template if GET. Does some 
		validation if POST and returns form agian if doesnt 
		validate and redirects to main admin page if it does
		"""
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

	@noindex
	def install(self):
		"""
		Returns installation page which sets up 
		the first user. 
		"""
		if runt_installed():
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
				install_runt(username=request.form['uname'], email=request.form['email'], password=request.form['password'])
				return "<h1>Installed!</h1>"

		return render_template('admin-install.html', error=err_return, values=values)
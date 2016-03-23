from peewee import *
from ..admin.auth import login_checker
from ..models.users_model import Users
from flask import render_template, request, redirect

#@login_checker
def index():
	"""
	This returns a list of all users
	"""
	return_list = Users.select(Users.id, Users.username, Users.level).order_by(Users.username)
	return render_template('admin-page.html', pageheader="Users", return_list=return_list)

#@login_checker
def add():
	"""
	This lets you add a new user
	"""
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

#@login_checker
def delete(uname):
	"""
	This asks for confirmation before 
	deleting the user
	"""

	"""
	Need to add something to prevent super admin from being deleted
	"""
	err_return = {}
	if request.method == 'POST':

		if request.form['delete'] == 'DELETE':
			Users.delete().where(Users.username == uname).execute()

			return redirect(url_for('admin_users_page'))

	return render_template('admin-delete-user.html', pageheader="Delete User", error=err_return)


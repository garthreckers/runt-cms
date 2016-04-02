"""
Group of functions to keep make 
some auth code easier
"""
import os
from functools import wraps
from flask import session, redirect, url_for
from .install import runt_installed
from ..models.users import Users
from werkzeug.security import check_password_hash

u = Users()

def auth(username, password):
	"""
	Function to quickly authenticate a user login
	"""
	get_user = u.get(Users.username == username)
	hash_pass = get_user.password
	if check_password_hash(hash_pass, password):
		id = get_user.id
		session.permanent = True
		session['uid'] = id
		return True
	return False

def check_username(username):
	"""
	Simple function to check if user already exists
	"""
	if u.select().where(Users.username == username).exists():
		return True
	return False

def logged_in():
	"""
	Simple function to check if user is logged in
	and returns user id as a string if is logged in
	"""
	if session.get('uid') is None:
		return False

	uid = session['uid']
		
	if uid:
		return str(uid)

	return False


def login_checker(func):
	"""
	Decorator to be used with Controllers to check if
	user is logged in and redirect to login page if not
	"""
	@wraps(func)
	def func_wrap(*args, **kwargs):
		if not runt_installed():
			return redirect(url_for('admin.install'))

		if logged_in():
			return func(*args, **kwargs)
		else:
			return redirect(url_for('admin.login'))
	return func_wrap

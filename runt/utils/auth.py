import os
from flask import session
from ..models.users_model import Users
from werkzeug.security import check_password_hash

u = Users()

def auth(username, password):
	get_user = u.get(Users.username == username)
	hash_pass = get_user.password
	if check_password_hash(hash_pass, password):
		id = get_user.id
		session.permanent = True
		session['uid'] = id
		return True
	return False

def check_username(username):
	if u.select().where(Users.username == username).exists():
		return True
	return False

def logged_in():
	if session.get('uid') is None:
		return False

	uid = session['uid']
		
	if uid:
		return str(uid)

	return False


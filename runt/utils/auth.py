import os
import jwt
from flask import session
from ..models.users_model import Users
from werkzeug.security import check_password_hash

u = Users()

def auth(username, password):
	get_user = u.get(Users.username == username)
	hash_pass = get_user.password
	if check_password_hash(hash_pass, password):
		id = get_user.id
		secret = os.urandom(24)
		token = jwt.encode({'user_id': id}, secret, algorithm='HS256')
		session['secret'] = secret
		session['token'] = token
		return True
	return False

def check_username(username):
	if u.select().where(Users.username == username).exists():
		return True
	return False

def logged_in():
	if session.get('token') is None or session.get('secret') is None:
		return False

	token = session['token']
	secret = session['secret']
	decode = jwt.decode(token, secret, algorithms=['HS256'])
		
	if decode:
		return str(decode['user_id'])

	return False


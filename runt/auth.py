from .models.users_model import Users
from werkzeug.security import check_password_hash

u = Users()

def auth(username, password):
	hash_pass = u.get(Users.username == username).password
	return check_password_hash(hash_pass, password)

def check_username(username):
	if u.select().where(Users.username == username).exists():
		return True
	return False


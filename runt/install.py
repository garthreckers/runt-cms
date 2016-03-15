from .models.base_model import mysql_db # Update later 
from .models.settings_model import Settings
from .models.users_model import Users

def check_install():
	if Settings.table_exists() or Users.table_exists():
		return False

	return True

def install(username, email, password):

	mysql_db.connect()
	mysql_db.create_tables([Settings, Users])

	u = Users()
	hash_pass = u.hash_password(password)
	u.create(email=email, username=username, password=hash_pass, level='admin')
	
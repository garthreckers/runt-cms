"""
Simple functions for installation
"""
from ..models.base_model import mysql_db # Update later 
from ..models.settings_model import Settings
from ..models.users_model import Users
from ..models.pages_model import Pages
from ..models.extensions_model import Extensions

def check_install():
	"""
	Simple function to check if Runt CMS is installed
	"""
	if Settings.table_exists() or Users.table_exists():
		return False

	return True

def install_runt(username, email, password):
	"""
	This is the installation function to create the first
	user and install the tables
	"""
	mysql_db.connect()
	mysql_db.create_tables([Settings, Users, Pages, Extensions])

	Settings.create(field='theme', value='default')

	u = Users()
	hash_pass = u.hash_password(password)
	u.create(email=email, username=username, password=hash_pass, level='admin')
	
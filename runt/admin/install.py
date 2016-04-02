"""
Simple functions for installation
"""
from ..models.base_model import mysql_db # Update later 
from runt.models import *

def runt_installed():
	"""
	Simple function to check if Runt CMS is installed
	"""
	if Users.table_exists():
		if Users.select().count() > 0:
			print('****************')
			return True	

	return False

def install_runt(username, email, password):
	"""
	This is the installation function to create the first
	user and install the tables
	"""
	u = Users()
	hash_pass = u.hash_password(password)
	u.create(email=email, username=username, password=hash_pass, level='admin')
	
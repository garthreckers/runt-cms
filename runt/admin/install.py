"""
Simple functions for installation
"""
from ..models.base_model import mysql_db # Update later 
from ..models import *
from ..utilities.mail import RuntMail

def runt_installed():
	"""
	Simple function to check if Runt CMS is installed
	"""
	if Users.table_exists():
		if Users.select().count() > 0:
			return True	

	return False

def install_runt(username, email, password, url):
	"""
	This is the installation function to create the first
	user and install the tables
	"""
	u = Users()
	hash_pass = u.hash_password(password)
	u.create(email=email, username=username, password=hash_pass, level='admin')
	
	RuntMail().new_user(email, username)

	s = Settings()
	s.create(field='homepage', value=url)
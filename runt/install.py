from .models.base_model import mysql_db # Update later 
from .models.settings_model import Settings

def install():
	mysql_db.connect()
	mysql_db.create_tables([Settings])
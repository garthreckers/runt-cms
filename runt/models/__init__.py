from .extensions import Extensions
from .pages import Pages
from .settings import Settings
from .users import Users
from .fields import Fields

if not Settings.table_exists():
	from .base_model import mysql_db

	mysql_db.connect()
	mysql_db.create_tables([Settings, Users, Pages, Extensions, Fields])
	
	Settings.create(field='theme', value='default')
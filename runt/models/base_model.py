"""
Sets up the base model to be extended by other models
"""
from ..config import DB
from peewee import *

mysql_db = MySQLDatabase(host=DB['DATABASE_HOST'], database=DB['DATABASE_DB'], user=DB['DATABASE_USER'], passwd=DB['DATABASE_PASSWORD'])

class BaseModel(Model):
	class Meta:
		database = mysql_db

	def show_tables():
		t = mysql_db.execute_sql("SHOW TABLES;")
		# t returns a list of tuples so show_tables will now return list of tables
		return [r[0] for r in t] 
		
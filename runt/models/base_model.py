"""
Sets up the base model to be extended by other models
"""
from ..config import DB
from peewee import *

mysql_db = MySQLDatabase(host=DB['DATABASE_HOST'], database=DB['DATABASE_DB'], user=DB['DATABASE_USER'], passwd=DB['DATABASE_PASSWORD'])

class BaseModel(Model):
    class Meta:
        database = mysql_db
        
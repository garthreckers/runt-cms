from .base_model import BaseModel
from peewee import *
from werkzeug.security import generate_password_hash

class Users(BaseModel):
    email = CharField(max_length=255, unique=True)
    username = CharField(max_length=30, unique=True)
    password = CharField(max_length=160)
    first_name = CharField(max_length=40, null=True)
    last_name = CharField(max_length=40, null=True)
    level = CharField(max_length=40)

    def hash_password(self, password):
    	return generate_password_hash(password)


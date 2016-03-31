from .base_model import BaseModel
from peewee import *

class Settings(BaseModel):
    field = CharField(max_length=60)
    value = CharField(max_length=120)
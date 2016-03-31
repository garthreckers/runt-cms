from .base_model import BaseModel
from peewee import *

class Extensions(BaseModel):
    name = CharField(max_length=255)
    active = BooleanField(default=False)

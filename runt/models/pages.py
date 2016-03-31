from .base_model import BaseModel
from peewee import *

class Pages(BaseModel):
    title = CharField(max_length=255)
    slug = CharField(unique=True)
    content = TextField(null=True)
    object_type = CharField(max_length=255)


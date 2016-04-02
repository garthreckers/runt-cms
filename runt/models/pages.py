import datetime
from .base_model import BaseModel
from peewee import *

class Pages(BaseModel):
    pub_date = DateTimeField(default=datetime.datetime.now())
    title = CharField(max_length=255)
    slug = CharField(unique=True, index=True)
    content = TextField(null=True)
    object_type = CharField(max_length=255)
    status = CharField(max_length=20, default='Published')


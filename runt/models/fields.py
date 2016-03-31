from .base_model import BaseModel
from peewee import *

class Fields(BaseModel):
    page_id = IntegerField(null=False)
    field_id = CharField(max_length=100)
    field_value = TextField()
    


from .base_model import BaseModel
from peewee import *

class Fields(BaseModel):
    page_id = IntegerField(null=False)
    field_id = CharField(max_length=100)
    field_value = TextField()
    field_type = CharField(max_length=50, null=True)
    secondary_meta_data = CharField(max_length=255, null=True)

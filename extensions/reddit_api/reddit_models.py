from peewee import CharField, IntegerField
from runt.models.base_model import BaseModel

class Reddit(BaseModel):
	title = CharField(max_length=100)
	post_id = IntegerField()

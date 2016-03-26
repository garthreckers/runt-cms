from runt.base_extension import BaseExtension
from flask import request, jsonify

class Extension(BaseExtension):
		
	def inject_variables(self, **kwargs):
		add_on = {"this_path": "Boom! This test is a success"}
		
		if kwargs:
			kwargs['this_path'] = "Boom! This test is a success"
			return kwargs
		
		return add_on
			
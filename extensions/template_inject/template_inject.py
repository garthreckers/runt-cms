from flask import request, jsonify

class Extension():
	def __init__(self):
		pass

	def inject_variables(self, **kwargs):
		add_on = {"this_path": "Boom! This test is a success"}
		
		if kwargs:
			kwargs['this_path'] = "Boom! This test is a success"
			return kwargs
		
		return add_on
			
from runt.base_extension import BaseExtension
from flask import request, jsonify

class Extension(BaseExtension):
		
	def inject_variables(self, **kwargs):
		add_on = {"this_path": "Boom! This test is a success"}
		
		if kwargs:
			kwargs['this_path'] = "Boom! This test is a success"
			return kwargs
		
		return add_on
			
	def inject_footer(self, injection):
		add_on = '''

		'''
		inject = injection + add_on
		return inject

	def inject_header(self, injection):
		add_on = '''
			<link rel="stylesheet" type="text/css" href="/template_inject/static/styles.css">
		'''
		inject = injection + add_on
		return inject
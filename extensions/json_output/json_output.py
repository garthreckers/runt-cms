from runt.base_extension import BaseExtension
from flask import request, jsonify

class Extension(BaseExtension):

	def before_template_load(self, *args, **kwargs):
		if kwargs:
			if request.args.get('output') == 'json':
				return jsonify(kwargs)
			return False
			
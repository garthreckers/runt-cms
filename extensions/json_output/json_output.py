from flask import request, jsonify

class Extension():
	def __init__(self):
		pass

	def before_template_load(self, **kwargs):
		if kwargs:
			if request.args.get('output') == 'json':
				return jsonify(kwargs)
			return False
			
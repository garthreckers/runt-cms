
class BaseExtension():
	def __init__(self):
		pass

	def before_template_load(self, *args, **kwargs):
		return False

	def inject_variables(self, **kwargs):
		return kwargs
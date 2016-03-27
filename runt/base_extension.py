
class BaseExtension():
	def __init__(self):
		pass

	def before_template_load(self, *args, **kwargs):
		return False

	def inject_variables(self, **kwargs):
		return kwargs

	def inject_header(self, injection):
		return ""

	def inject_footer(self, injection):
		return ""

	"""
	Auth stuff
	API stuff
	Admin area stuff
	on activation script
	on deactivation script
	
	"""
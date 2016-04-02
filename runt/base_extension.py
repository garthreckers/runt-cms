"""
This Base Class is ment to be extended by new Extensions
"""

class BaseExtension():
	"""
	class that returns the appropriate value if the method
	is not used

	ideas for new stuff:

	Auth stuff
	API stuff
	Admin area stuff
	on activation script
	on deactivation script

	"""
	def __init__(self):
		pass

	def install(self):
		return False

	def before_template_load(self, *args, **kwargs):
		"""
		Return False because load_template will check if
		the return value is not False
		"""
		return False

	def inject_variables(self, **kwargs):
		"""
		If no new variables are added, it returns the 
		original kwargs
		"""
		return kwargs

	def inject_header(self, injection):
		"""
		returns blank since any new method calls will append to this
		"""
		return ""

	def inject_footer(self, injection):
		"""
		returns blank since any new method calls will append to this
		"""
		return ""

"""
Extension Wrappers
"""
from extensions import *
from flask import render_template

def load_template(template, **kwargs):
	"""
	This needs to be fixed so that the call to the class and method
	are dynamic based on which extensions are active
	"""
	# use var exts to access all plugins

	return_kwargs = template_inject.Extension().inject_variables(**kwargs)

	e_before = json_output.Extension().before_template_load(**(return_kwargs))
	if e_before:
		return e_before
	return render_template(template, **(return_kwargs))
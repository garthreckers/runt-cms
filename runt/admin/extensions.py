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
	e = json_output.Extension()
	e_before = e.before_template_load(**kwargs)
	if e_before:
		return e_before
	return render_template(template, **kwargs)
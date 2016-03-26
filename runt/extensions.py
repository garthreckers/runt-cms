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

	""" loop through inject_variables' to add any variables """
	return_kwargs = kwargs
	print(active_exts)
	for e in active_exts:
		return_kwargs = eval(e).Extension().inject_variables(**kwargs)

	""" loop through before_template_load's and returns if need be """
	for e in active_exts:
		e_before = eval(e).Extension().before_template_load(**(return_kwargs))
	
		if e_before:
			return e_before
	
	return render_template(template, **(return_kwargs)) 
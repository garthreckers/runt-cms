"""
Extension Wrappers
"""
from extensions import *
import importlib
import sys
from runt.models import Extensions as Ext_Model
from flask import render_template


def load_template(template, **kwargs):
	"""
	This needs to be fixed so that the call to the class and method
	are dynamic based on which extensions are active
	"""	

	""" loop through inject_variables to add any variables """
	return_kwargs = kwargs

	active_e = Ext_Model.select().where(Ext_Model.active == True)

	install_ext()

	for e in active_e:
		return_kwargs = eval(e.name).Extension().inject_variables(**kwargs)

	""" loop through before_template_load's and returns if need be """
	for e in active_e:
		e_before = eval(e.name).Extension().before_template_load(**(return_kwargs))
	
		if e_before:
			return e_before
	
	return render_template(template, **(return_kwargs))

def inject_footer():
	
	inject = ""

	active_e = Ext_Model.select().where(Ext_Model.active == True)

	for e in active_e:
		e_return = eval(e.name).Extension().inject_footer(inject)
		inject = inject + e_return
		
	return dict(runt_footer=inject)

def inject_header():
	
	inject = ""

	active_e = Ext_Model.select().where(Ext_Model.active == True)

	for e in active_e:
		e_return = eval(e.name).Extension().inject_header(inject)
		inject = inject + e_return
		
	return dict(runt_header=inject)






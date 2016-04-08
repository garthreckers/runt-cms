"""
Extension Wrappers

"""
import sys
import pip
import importlib
from extensions import *
from .extensions_install import install_ext
from peewee import *
from .models import Extensions as Ext_Model
from flask import render_template
from .models.base_model import mysql_db, BaseModel

def module_install_script(ext):

	e_mod = getattr(sys.modules[__name__], ext)
	_e = e_mod.Extension()

	_e.install_scripts()

	_e_model = _e.install_models()
	
	if _e_model:
		_e_list = []
		for _e_m in _e_model:
			if not _e_m.table_exists():
				_e_list.append(_e_m)

		mysql_db.connect()
		mysql_db.create_tables(_e_list)
	
	return

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
		e_mod = getattr(sys.modules[__name__], e.name)
		return_kwargs = e_mod.Extension().inject_variables(**kwargs)

	""" loop through before_template_load's and returns if need be """
	for e in active_e:
		e_mod = getattr(sys.modules[__name__], e.name)
		e_before = e_mod.Extension().before_template_load(**(return_kwargs))
	
		if e_before:
			return e_before
	
	return render_template(template, **(return_kwargs))

def inject_footer():
	
	inject = ""

	active_e = Ext_Model.select().where(Ext_Model.active == True)

	for e in active_e:
		e_mod = getattr(sys.modules[__name__], e.name)
		e_return = e_mod.Extension().inject_footer(inject)
		inject = inject + e_return
		
	return dict(runt_footer=inject)

def inject_header():
	
	inject = ""

	active_e = Ext_Model.select().where(Ext_Model.active == True)

	for e in active_e:
		e_mod = getattr(sys.modules[__name__], e.name)
		e_return = e_mod.Extension().inject_header(inject)
		inject = inject + e_return
		
	return dict(runt_header=inject)

import os, sys
import importlib
from runt.models.extensions_model import Extensions

EXT_PATH = os.path.dirname(os.path.abspath(__file__))
ext_files = os.listdir(EXT_PATH)

"""

rework this code. right now the pycache is throwing this off
maybe:
	- active_ext list is based on DB
	- DB is updated everytime /admin/extensions is loaded

"""

exts = Extensions.select(Extensions.name)

exts_names = []
for e in exts:
	exts_names.append(e.name)

def install_ext():
	for e in ext_files:
		if not e.startswith('.') and not e.startswith('_'):
			import_e = 'extensions.' + e + '.' + e
			__import__(import_e)
			if e not in exts_names:
				Extensions().create(name=e)
	
	for e in exts_names:
		if e not in ext_files:
			Extensions().delete().where(Extensions.name == e).execute()

install_ext()

	
	

		


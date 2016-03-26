import os
from runt.models.extensions_model import Extensions


EXT_PATH = os.path.dirname(os.path.abspath(__file__))
ext_files = os.listdir(EXT_PATH)

"""

rework this code. right now the pycache is throwing this off
maybe:
	- active_ext list is based on DB
	- DB is updated everytime /admin/extensions is loaded

"""
exts = []
active_exts = []
for e in ext_files:
	if not e.startswith('.') and not e.startswith('_'):
		if (Extensions.select().where((Extensions.name == e) & (Extensions.active == True)).exists()):
			active_exts.append(e)
		exts.append(e)
		import_e = 'extensions.' + e + '.' + e
		__import__(import_e)
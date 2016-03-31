"""
Initializes extensions and runs install function
on start up and restart
"""
import os
import sys
import importlib
from runt.models.extensions import Extensions

EXT_PATH = os.path.dirname(os.path.abspath(__file__))
EXT_FILES = os.listdir(EXT_PATH)

EXTS = Extensions.select(Extensions.name)

EXTS_NAMES = []
for e in EXTS:
	EXTS_NAMES.append(e.name)

def install_ext():
	"""
	First - checks the files in /extensions to make sure they are
	in the DB
	Second - checks the extensions in the DB to make sure they are
	in the directory
	"""
	for _ef in EXT_FILES:
		if not _ef.startswith('.') and not _ef.startswith('_'):
			import_e = 'extensions.' + _ef + '.' + _ef
			__import__(import_e)
			if _ef not in EXTS_NAMES:
				Extensions().create(name=_ef)

	for _en in EXTS_NAMES:
		if _en not in EXT_FILES:
			Extensions().delete().where(Extensions.name == _en).execute()

install_ext()

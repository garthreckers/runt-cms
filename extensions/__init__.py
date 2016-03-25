import os

ext_files = os.listdir(os.path.dirname(os.path.abspath(__file__)))

exts = []
for e in ext_files:
	if not e.startswith('.') and not e.startswith('_'):
		exts.append(e)
		import_e = 'extensions.' + e + '.' + e
		__import__(import_e)
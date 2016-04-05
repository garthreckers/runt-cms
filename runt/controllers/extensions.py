import os
import json
import config
from ..admin.auth import login_checker, check_username, auth
from runt.utils import noindex
from ..admin.install import runt_installed, install_runt
from flask import render_template, request, redirect, url_for
from ..models import Settings

class ExtensionController():
	def __init__(self):
		pass

	def settings(self, ext_name):
		"""
		Need to add settings db read
		"""

		path_to_json = config.ROOT_DIR + '/extensions/' + ext_name + '/settings.json'

		settings = None
		with open(path_to_json, "r") as s:
			settings = json.loads(s.read())

		for s in settings:
			_combo = ext_name + '--' + s

			_setting = Settings().select().where(Settings.field == _combo)
			_init_value = _setting.get().value if _setting.exists() else None

			if request.method == 'POST':	
				_v = request.form[_combo]
				if _v != _init_value:
					settings[s]['value'] = _v
					if _setting.exists():
						_su = Settings().update(value=_v).where(Settings.field == _combo)
						_su.execute()
						pass
					else:
						Settings().create(field=_combo, value=_v)
				else:
					settings[s]['value'] = _init_value
			else:
				settings[s]['value'] = _init_value

		return render_template("extensions-settings.html", settings=settings, ext_name=ext_name)
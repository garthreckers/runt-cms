import os
import json
import config
from ..admin.auth import login_checker, check_username, auth
from runt.utils import noindex
from ..admin.install import runt_installed, install_runt
from flask import render_template, request, redirect, url_for
from ..models import Settings, Extensions

class ExtensionController():
	def __init__(self):
		pass		

	def index(self):
		if request.method == 'POST':
			name = request.form['ext_name']
			activation = True if request.form['activation'] == 'activate' else False

			select_ext = Extensions.select().where(Extensions.name == name)

			if select_ext.exists():
				Extensions.update(active=activation).where(Extensions.name == name).execute()
			else:
				Extensions.create(name=name, active=activation)

			if activation:
				module_install_script(name)

			#return redirect(url_for('extensions.admin_install_extensions'))

			
		exts = Extensions.select().order_by(+Extensions.name)


		exts_dict = {}
		for e in exts:
			_exts_temp_dict = {}
			_e_path = config.ROOT_DIR + "/extensions/" + e.name + "/extension.json"
			
			if os.path.exists(_e_path):
				with open(_e_path, "r") as f:
					_exts_json = json.loads(f.read())['extension_details']
					_exts_temp_dict.update(_exts_json)

			settings_json = config.ROOT_DIR + '/extensions/' + e.name + '/settings.json'

			_exts_temp_dict['has_settings'] = os.path.exists(settings_json)

			if e.active == True:
				_exts_temp_dict.update({"active": True})
				exts_dict.update({e.name: _exts_temp_dict})
			else:
				_exts_temp_dict.update({"active": False})
				exts_dict.update({e.name: _exts_temp_dict})

		return render_template("extensions.html", pageheader="Extensions", extensions=exts_dict)


	def settings(self, ext_name):
		settings_json = config.ROOT_DIR + '/extensions/' + ext_name + '/settings.json'

		if not os.path.exists(settings_json): 
			return render_template('404.html', pageheader="404 - Page Not Found"), 404

		settings = None
		with open(settings_json, "r") as s:
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

		e_path = config.ROOT_DIR + "/extensions/" + ext_name + "/extension.json"
			
		if os.path.exists(e_path):
			with open(e_path, "r") as f:
				_exts_json = json.loads(f.read())['extension_details']

		pageheader = _exts_json['name'] or ext_name

		pageheader = pageheader + ' Settings'


		return render_template("extensions-settings.html", settings=settings,\
									ext_name=ext_name, pageheader=pageheader)
import os
import json
import sys
import config
from flask import Blueprint, send_from_directory,\
					request, render_template, redirect, url_for
from runt.models import Settings, Extensions
from runt.extensions import inject_header, inject_footer,\
								module_install_script
from ..controllers import ExtensionController

extensions = Blueprint('extensions', __name__)

e = ExtensionController()

@extensions.route('/<ext>/static/<path:filename>')
def ext_static_files(ext, filename):
	theme = Settings.select(Settings.value).where(Settings.field == 'theme').get().value
	static_path = config.ROOT_DIR + '/extensions/' + ext + '/static'
	return send_from_directory(static_path, filename)

@extensions.route('/admin/extensions/<ext>/settings', methods=['GET', 'POST'], strict_slashes=False)
def admin_extenstions_settings(ext):
	return e.settings(ext)

@extensions.route("/admin/extensions", methods=['GET', 'POST'], strict_slashes=False)
def admin_extensions():

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

		if e.active == True:
			_exts_temp_dict.update({"active": True})
			exts_dict.update({e.name: _exts_temp_dict})
		else:
			_exts_temp_dict.update({"active": False})
			exts_dict.update({e.name: _exts_temp_dict})

	return render_template("extensions.html", pageheader="Extensions", extensions=exts_dict)


"""
Basically when admin/extensions/install is hit, the iframe will fail but will successfully
restart the python server. 
"""
@extensions.route("/admin/extensions/install")
def admin_install_extensions():
	return render_template("extensions-install.html", pageheader="Processing...")

@extensions.route("/admin/restart_app")
def admin_restart_app():
	python = sys.executable
	os.execl(python, python, * sys.argv)
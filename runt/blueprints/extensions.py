import os
import json
import sys
import config
from flask import Blueprint, send_from_directory,\
					request, render_template, redirect, url_for
from runt.models import Settings
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
	return e.index()


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
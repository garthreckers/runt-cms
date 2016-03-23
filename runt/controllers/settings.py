import os
import json
from ..models.settings_model import Settings
from ..admin.auth import login_checker
from flask import render_template, request
from ..config import RUNT_ROOT

#@login_check
def index():
	return render_template('admin-base.html', pageheader="Main Settings Page")

def themes():
	"""
	This is the theme selector page. Its checks the 
	/themes/ dir for folders and then grabs stuff like
	author, name, copyright, etc. from theme.json. 
	"""
	theme_folders = os.listdir(RUNT_ROOT + '/themes/')

	themes = {}
	for t in theme_folders:
		if not t.startswith("."):
			_t_path = RUNT_ROOT + '/themes/' + t + '/theme.json'
			with open(_t_path, 'r') as j:
				theme_json = json.loads(j.read())
				themes[t] = theme_json['author']

	get_theme = Settings.select().where(Settings.field == 'theme').get()
	current_theme = get_theme.value

	print(themes)
	if request.method == 'POST':
		new_theme = request.form['theme']
		get_theme.value = new_theme
		get_theme.save()

		""" Change current theme to update theme """
		current_theme = new_theme

	return render_template('admin-themes.html', pageheader="Pick a theme", themes=themes, current=current_theme)
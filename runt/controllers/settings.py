import os
import json
from ..models import Settings
from runt.utils import noindex
from ..admin.auth import login_checker
from flask import render_template, request
from config import ROOT_DIR

class SettingsController():
	def __init__(self):
		pass
	#@login_check
	@noindex
	def index(self):
		return render_template('admin-base.html', pageheader="Main Settings Page")

	@noindex
	def themes(self):
		"""
		This is the theme selector page. Its checks the 
		/themes/ dir for folders and then grabs stuff like
		author, name, copyright, etc. from theme.json. 
		"""
		theme_folders = os.listdir(ROOT_DIR + '/themes/')

		themes = {}
		for t in theme_folders:
			if not t.startswith("."):
				_t_path = ROOT_DIR + '/themes/' + t + '/theme.json'
				with open(_t_path, 'r') as j:
					theme_json = json.loads(j.read())
					themes[t] = theme_json['theme_details']

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
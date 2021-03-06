import os
import json
from peewee import *
from flask import render_template, request
from config import ROOT_DIR
from ..models import Settings
from ..utilities.decorators import noindex, login_checker

class SettingsController():
	def __init__(self):
		pass

	#@login_check
	@noindex
	def index(self):
		runt_settings = {
			"site_name": {
				"type": "text",
				"name": "Site Name"
			},
			"homepage": {
				"type": "url",
				"name": "Homepage URL"
			}
		}

		for r in runt_settings:
			if request.method == 'POST':
				if request.form[r]:
					if Settings().select().where(Settings.field == r).exists():
						(Settings()
							.update(value=request.form[r])
							.where(Settings.field == r)
							.execute())
					else:
						Settings().create(field=r, value=request.form[r])

			if Settings().select().where(Settings.field == r).exists():
				_v = Settings().select(Settings.value).where(Settings.field == r).get().value
				runt_settings[r]['value'] = _v

		return render_template('settings.html', pageheader="Settings", runt_settings=runt_settings)

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

		return render_template('themes.html', pageheader="Pick a theme", themes=themes, current=current_theme)

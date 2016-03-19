from ..models.settings_model import Settings
from ..admin.auth import login_checker
from flask import render_template, request

#@login_check
def index():
	return render_template('admin-base.html', pageheader="Main Settings Page")

def themes():
	# hardcoded for now
	themes = ('default', 'option_2')
	get_theme = Settings.select().where(Settings.field == 'theme').get()
	current_theme = get_theme.value
	if request.method == 'POST':
		new_theme = request.form['theme']
		get_theme.value = new_theme
		get_theme.save()
		
		""" Change current theme to update theme """
		current_theme = new_theme

	return render_template('admin-themes.html', pageheader="Pick a theme", themes=themes, current=current_theme)
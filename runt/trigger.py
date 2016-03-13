"""

Builds the basics for Runt

"""
import jinja2
from flask import Flask, render_template

trigger = Flask(__name__)

trigger.debug = True

theme_loader = jinja2.ChoiceLoader([
	    trigger.jinja_loader,	
		jinja2.FileSystemLoader([
				'runt/themes',
				'runt/admin/templates'
			])
	])
trigger.jinja_loader = theme_loader


@trigger.route("/admin")
def admin():
	return render_template('admin-main.html')

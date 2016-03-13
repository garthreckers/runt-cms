"""

Builds the basics for Runt

"""
import jinja2
from . import config
from flask import Flask, render_template
from flask.ext.mysqldb import MySQL
#from . import install

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


mysql = MySQL()

trigger.config.update(config.DB)

mysql.init_app(trigger)

@trigger.route("/admin")
def admin():
	return render_template('admin-main.html')

@trigger.route("/install")
def install():

	query = "CREATE TABLE settings (\
		id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
		field VARCHAR(50) NOT NULL,\
		value VARCHAR(120),\
		)"

	cursor = mysql.connect().cursor()
	cursor.execute(query)

	return "installed maybe"

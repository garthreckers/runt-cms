#!/bin/env/Python3
from flask.ext.mysqldb import MySQL
from . import config
from .trigger import trigger


def build():
	query = "CREATE TABLE settings (\
		id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,\
		field VARCHAR(50) NOT NULL,\
		value VARCHAR(120),\
		)"
	try:
		cursor = mysql.connect().cursor()
		cursor.execute(query)
	except e:
		raise e

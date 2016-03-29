import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNT_ROOT = ROOT_DIR + '/runt'
RUNT_UPLOADS = ROOT_DIR + '/uploads/'

DB = {
	"MYSQL_DB_HOST" : "localhost",
	"MYSQL_DB_NAME" : "Your Database Name",
	"MYSQL_DB_USER" : "Your Database User",
	"MYSQL_DB_PASSWORD" : "Your Database Password"
}
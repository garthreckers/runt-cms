from runt.trigger import trigger
from flask import render_template

@trigger.route("/")
def home():
	return render_template('placeholder.html')


if __name__ == "__main__":
	trigger.run()
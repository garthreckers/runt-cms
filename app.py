from flask import Flask, render_template
app = Flask(__name__)

app.debug = True

@app.route("/")
def home():
	return "Homepage"

@app.route("/admin")
def admin():
	return render_template('admin/main-admin.html')

if __name__ == "__main__":
	app.run()
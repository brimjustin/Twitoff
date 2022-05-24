from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('base.html', title='Home')

app_title = "Twitoff DS38"

@app.route('/test')
def test():
	return f"<p>This is a page for {app_title}<p>"

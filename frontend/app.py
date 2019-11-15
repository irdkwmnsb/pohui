from flask import Flask
from flask import render_template, request

from os import path
import secrets

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './uploads'


@app.route('/')
def index():
	return render_template('index.html')



@app.route('/api/register')
def register():
	""" api call to register new voice """
	if request.method == "POST":
		voice = request.files["voice"]
		filename = secrets.token_hex(32)
		file.save(path.join(app.config["UPLOAD_FOLDER"], filename))


	else:
		return 666


@app.route('/api/recognize')
def recognize():
	""" api call to recognize a voice """
	if request.method == "POST":
		voice = request.files["voice"]
		filename = secrets.token_hex(32)
		file.save(path.join(app.config["UPLOAD_FOLDER"], filename))


	else:
		return 666
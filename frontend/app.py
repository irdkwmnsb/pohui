from flask import Flask
from flask import render_template, request, jsonify

from os import path
import secrets
import sys; sys.path.append('../pohuy-ai/') # i love my mom

from pohuy import pohuy

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = '/tmp'


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/api/listusers')
def listusers():
	model = pohuy()
	users = [
		{
			"name": user[0],
			"age": user[1],
			"gender": user[2]
		} for user in model.listusers()
	]

	return jsonify(users), 200


@app.route('/api/register', methods=["POST"])
def register():
	""" api call to register new voice """
	if "voice" not in request.files or not all([x in request.values for x in ["name", "age", "gender"]]):
		return 400

	if type(request.values["name"]) is not str:
		return 400

	if type(request.values["age"]) is not int:
		return 400

	if request.values["gender"] not in [0, 1]:
		return 400

	name, age, gender = request.values["name"], request.values["age"], request.values["gender"]
	

	voice = request.files["voice"]
	filename = path.join(app.config["UPLOAD_FOLDER"], secrets.token_hex(24))
	file.save(filename)

	model = pohuy()
	model.registerUser(name, age, gender, filename)

	return 200


@app.route('/api/recognize', methods=["POST"])
def recognize():
	""" api call to recognize a voice """
	# if request.method == "POST":
	if "voice" not in request.files or not all([x in request.values for x in ["age", "gender"]]):
		return 400

	if type(request.values["age"]) is not int:
		return 400

	if request.values["gender"] not in [0, 1]:
		return 400

	age, gender = request.files["age"], request.files["gender"]

	voice = request.files["voice"]
	filename = path.join(app.config["UPLOAD_FOLDER"], secrets.token_hex(24))
	file.save(filename)

	model = pohuy()
	person = model.predict(age, gender, filename)

	return 200, person

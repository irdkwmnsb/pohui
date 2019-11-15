from flask import Flask
from flask import render_template, request, jsonify

from os import path
import secrets
import sys; sys.path.append('../pohuy-ai/') # i love my mom

from pohuy import pohui

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = '/tmp'

import string
alphabet_whitelist = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/api/listusers')
def listusers():
	model = pohui()
	users = [
		{
			"name": user["name"],
			"age": user["age"],
			"gender": user["gender"],
		} for user in model.getRegistered()
	]

	return jsonify(users), 200


@app.route('/api/register', methods=["POST"])
def register():
	""" api call to register new voice """
	if "voice" not in request.files or not all([x in request.values for x in ["name", "age", "gender"]]):
		return "need more parameters", 400

	if type(request.values["name"]) is not str and len(request.values["name"]) >= 4:
		return "name must be a string", 400

	name = request.values["name"]
	if not all([x in alphabet_whitelist for x in name]):
		return "bad symbols in name", 400

	try:
		age = int(request.values["age"])
	except Exception:
		return "age must be an integer", 400

	try:
		gender = int(request.values["gender"])
	except Exception:
		return "gender must be an integer", 400

	if gender not in [0, 1]:
		return "gender must be 0 or 1", 400

	
	print("checks ok")
	voice = request.files["voice"]
	filename = path.join(app.config["UPLOAD_FOLDER"], "rec_" + secrets.token_hex(24) + ".wav")
	voice.save(filename)

	# print(f"register({name}, {age}, {gender}, {filename})")
	model = pohui()
	for _ in range(10):
		try:
			model.registerUser(name, age, gender, filename)
			break
		except Exception:
			import traceback
			traceback.print_exc()
			pass
	else:
		return "твой голос хуйня", 400

	return "ok", 200


@app.route('/api/recognize', methods=["POST"])
def recognize():
	""" api call to recognize a voice """
	if "voice" not in request.files or not all([x in request.values for x in ["age", "gender"]]):
		return "need more parameters", 400

	try:
		age = int(request.values["age"])
	except Exception:
		return "age must be an integer", 400

	try:
		gender = int(request.values["gender"])
	except Exception:
		return "gender must be an integer", 400

	if gender not in [0, 1]:
		return "gender must be 0 or 1", 400

	# age, gender = request.files["age"], request.files["gender"]
	print("checks done")

	voice = request.files["voice"]
	filename = path.join(app.config["UPLOAD_FOLDER"], "rec_"+secrets.token_hex(24)+".wav")
	voice.save(filename)

	model = pohui()
	person = model.predict(age, gender, filename)

	return person, 200

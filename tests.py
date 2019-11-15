# requres requests

import requests as req
import secrets

URL = 'http://localhost:5000/'
name = ''

def test_list_users():
	"""listusers"""
	try:
		users = req.get(URL+"api/listusers").json()
		if len(users) > 0 and all([x in users[0] for x in ["name", 'age', 'gender']]):
			return "OK"
	except Exception:
		return "NOT OK"

def test_regster():
	"""register"""
	global name

	try:
		name = "lox_test_"+str(secrets.token_hex(8))
		resp = req.post(URL+"api/register",
			data={"name": name, "age": 28, "gender": 1},
			files={'voice': open('test.wav', 'rb')}
			)
		# print(resp.text)
		# print(resp.status_code)
		if resp.status_code == 200:
			return "OK"
		else:
			return "NOT OK"
	except Exception:
		return "NOT OK"

def test_recog():
	"""recognition"""
	try:
		resp = req.post(URL+"api/recognize",
			data={"age": 28, "gender": 1},
			files={'voice': open('test.wav', 'rb')}
			)
		print(resp.text)
		# print(resp.status_code)
		if resp.status_code == 200:
			return "OK"
		else:
			return "NOT OK"
	except Exception:
		return "NOT OK"


funcs = [
	test_regster,
	test_list_users,
	test_recog
]

for f in funcs:
	print(f.__doc__, f())
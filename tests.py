# requres requests

import requests as req

URL = 'http://localhost:5000/'

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

	try:
		resp = req.post(URL+"api/register",
			data={"name": "lox_test", "age": 28, "gender": 1},
			files={'voice': open('test.wav', 'rb')}
			)
		print(resp.text)
		print(resp.status_code)
		return "OK"
	except Exception:
		return "NOT OK"

funcs = [
	test_regster,
	# test_list_users
]

for f in funcs:
	print(f.__doc__, f())
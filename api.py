from flask import request
from config import config
from server import app
import json


@app.route('/', methods=['POST', 'GET'])
def hello():
	return json.dumps({"message": "hello"})


@app.route('/get-book-review', methods=['POST'])
def get_book_review():
	return json.dumps({"message": "hello"})


if __name__ == '__main__':
	app.run(
		host=config.get_config("flask", "host"),
		port=config.get_config("flask", "port"),
		debug=False,
		use_reloader=False
	)
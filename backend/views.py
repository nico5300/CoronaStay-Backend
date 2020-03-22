from datetime import datetime

from flask import request, abort

from backend import app
from flask_json import json_response

import uuid


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/test/")
def testBla():
    return json_response(time=datetime.now())


@app.route("/register/", methods=["POST"])
def register():
    print(request.is_json)
    if not request.is_json:
        abort(400)

    data = request.get_json(force=True)
    username = data["username"]
    password = data["password"]

    user_uuid = uuid.uuid1()

    # TODO: Check if already exists
    # TODO: Save that scheissdregg

    response_dict = {"user_uuid": user_uuid, "username_test_pls_remove_me": username}

    return json_response(**response_dict)


@app.route("/story/", methods=["POST"])
def story():
    pass

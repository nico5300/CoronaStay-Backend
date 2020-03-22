from datetime import datetime
from functools import wraps
from flask import request, abort, g

from backend import app
from backend.models import User
from flask_json import json_response

import uuid


def check_api_key(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user is not None:
        g.user = User
        return True
    else:
        return False


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        if data is None:
            abort(400)
        try:
            api_key = data["api_key"]
            if check_api_key(api_key):
                g.api_key = api_key
                return f(*args, **kwargs)
            else:
                abort(401)
        except KeyError:
            abort(400)
    return decorated_function


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

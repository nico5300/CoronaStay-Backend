from datetime import datetime
from functools import wraps
from flask import request, abort, g
from sqlalchemy.exc import IntegrityError
from backend import app, db
from backend.models import User, Story, Panel
from flask_json import json_response
import uuid
import base64
import hashlib
import os

from backend.models import User
from config import IMAGE_ROOT


def getDataIfValid():
    if not request.is_json:  # Kann man vllt entfernen, mal sehen
        abort(400)
    return request.get_json(force=True)  # force=True, damit mime-type nicht beachtet wird


def check_api_key(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user is not None:
        g.user = user
        return True
    else:
        return False


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = getDataIfValid()
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


@app.route("/register/", methods=["POST"])
def register():
    data = getDataIfValid()

    if "username" not in data:
        abort(422)  # Unprocessable Entity

    username = data["username"]
    user_uuid = uuid.uuid4()
    new_user = User(name=username, api_key=user_uuid)

    try:
        db.session.add(new_user)
    except IntegrityError:
        abort(409)  # 409: Conflict
        db.session.commit()

    return json_response(api_key=user_uuid)


@app.route("/story/", methods=["POST"])
@api_key_required
def story():
    data = getDataIfValid()

    if ("title" not in data) or ("start_panel" not in data):
        abort(422)  # Unprocessable Entity

    img_data = base64.b64decode(data["start_panel"])
    sha = hashlib.sha256()
    sha.update(img_data)
    hash_str = sha.digest().hex()
    target_folder, file_name = os.path.join(IMAGE_ROOT, hash_str[:2], hash_str[2:4]), hash_str[4:] + ".png"
    os.makedirs(target_folder, exist_ok=True)
    file = open(os.path.join(target_folder, file_name), mode="wb")      # potentially unsafe, if identical pics..
    file.write(img_data)
    file.close()

    print("jasdfjljdöaf",g.user.name)
    new_story = Story(user_name=g.user.name, title=data["title"])
    file_name_on_server = os.path.join(hash_str[:2], hash_str[2:4], file_name)

    db.session.add(new_story)
    db.session.commit()

    new_panel = Panel(story_id=new_story.id_, file_name=file_name_on_server)
    db.session.add(new_panel)
    db.session.commit()

    return json_response(story_id=new_story.id_)


@app.route("/story/<int:story_id>/", methods=["GET"])
@api_key_required
def get_story(story_id):
    story = Story.query.filter_by(id_=story_id).first()
    if not story:
        abort(404)
    return json_response(data_={
        "title": story.title,
        "panels": [p.file_name for p in story.panels]
    })


@app.route("/stories/", methods=["GET"])
@api_key_required
def get_stories():
    stories = Story.query.all()
    teasers = []
    for st in stories:
        teasers.append({
            "title": st.title,
            "start_panel": st.panels[0].file_name
        })
    return json_response(data_={
        "stories": teasers
    })

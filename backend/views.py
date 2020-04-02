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


@app.before_request
def check_load_json():
    # if content type is not application/json or data is not parsable, this will return none
    json_data = request.get_json(cache=True, silent=True)
    if json_data is None:
        abort(400)
    g.json_data = json_data


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
        try:
            api_key = g.json_data["api_key"]
            if check_api_key(api_key):
                g.api_key = api_key
                return f(*args, **kwargs)
            else:
                abort(401)
        except KeyError:
            abort(400)

    return decorated_function


@app.route("/register/", methods=["POST"])
def register():
    if "username" not in g.json_data:
        abort(422)  # Unprocessable Entity

    username = g.json_data["username"]
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
    if ("title" not in g.json_data) or ("start_panel" not in g.json_data):
        abort(422)  # Unprocessable Entity

    img_data = base64.b64decode(g.json_data["start_panel"])
    sha = hashlib.sha256()
    sha.update(img_data)
    hash_str = sha.digest().hex()
    target_folder = os.path.join(app.config.get('IMAGE_ROOT'), hash_str[:2], hash_str[2:4])
    os.makedirs(target_folder, exist_ok=True)
    file_name = hash_str[4:] + ".png"
    file = open(os.path.join(target_folder, file_name), mode="wb")  # identical images overwritten
    file.write(img_data)
    file.close()

    new_story = Story(user_name=g.user.name, title=g.json_data["title"])
    db.session.add(new_story)
    db.session.commit()

    file_name_on_server = os.path.join(
        app.config.get('IMAGE_SERVE_ROOT'),
        hash_str[:2], hash_str[2:4],
        file_name)
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

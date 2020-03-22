from backend import db

class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    api_key = db.Column(db.String, unique=True)
    stories = #TODO


class Story(db.Model):
    story_id = db.Column(db.String, primary_key=True)
    creator = #TODO
    title = db.Column(db.String)

class Panel(db.Model):
    panel_id = db.Column(db.Integer, autoincrement=True)
    file_name = db.Column(db.String, unique=True)


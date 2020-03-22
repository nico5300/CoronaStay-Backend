from backend import db


class User(db.Model):
    name = db.Column(db.String, primary_key=True)
    api_key = db.Column(db.String, unique=True)
    stories = db.relationship('Story', backref='user')


class Story(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, db.ForeignKey('user.name'))
    title = db.Column(db.String)
    panels = db.relationship('Panel', backref='story')


class Panel(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id_'))
    file_name = db.Column(db.String, unique=True)


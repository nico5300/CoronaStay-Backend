from backend import db

class User(db.Model):
    name = db.Column(db.String, primary_key=True)
    api_key = db.Column(db.String, unique=True)
    stories = db.Relationship('Story', backref='user')


class Story(db.Model):
    _id = db.Column(db.String, primary_key=True)
    user_name = db.Column(db.String, db.ForeignKey('user.name'))
    title = db.Column(db.String)
    panels = db.Relationship('Panel', backref='story')

class Panel(db.Model):
    panel_id = db.Column(db.Integer, autoincrement=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story._id'))
    file_name = db.Column(db.String, unique=True)


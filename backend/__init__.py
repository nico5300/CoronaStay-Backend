from flask import Flask
from flask_json import FlaskJSON
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
json = FlaskJSON(app)
app.config.from_object(__name__ + '.settings')  # default settings
app.config.from_object('config')  # deployment specific settings (no version control)

db = SQLAlchemy(app)

import backend.models  # noqa
import backend.views  # noqa

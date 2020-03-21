
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# settings used for development

SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(_basedir, 'db.sqlite')

del os


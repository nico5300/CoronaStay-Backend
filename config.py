
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# settings used for development

SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'db.sqlite')

IMAGE_ROOT = os.path.join(_basedir, "images/")  # where panel images should be stored
IMAGE_SERVE_ROOT = "/images/"  # relative path under which images will be served

del os

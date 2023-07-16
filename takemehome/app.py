import os
from flask import Flask
from .api import api
from .model import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)
api.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()

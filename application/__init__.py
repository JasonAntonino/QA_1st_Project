from flask import flask
from flask_sqlalchemy import flask_sqlalchemy

app = Flask(__name__)

db = SQLAlchemy(app)

from application import routes
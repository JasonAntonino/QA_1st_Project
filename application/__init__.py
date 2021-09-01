from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Creates a local database (*****NEEDS TO BE CHANGED TO AWS MYSQL DATABASE FOR PRODUCTION*****)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"     

#Creates a secret key which is used by the forms (*****NEEDS TO BE CHANGED AND PUT IN AN ENVIRONMENT VARIABLE*****)
app.config['SECRET_KEY'] = '1234567abc'

db = SQLAlchemy(app)        #Creates the database object

from application import routes
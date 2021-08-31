from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Creates a local database (*****NEEDS TO BE CHANGED TO AWS MYSQL DATABASE FOR PRODUCTION*****)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"     

db = SQLAlchemy(app)        #Creates the database object

from application import routes
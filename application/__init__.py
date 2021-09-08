from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

#Creates a local database (*****NEEDS TO BE CHANGED TO AWS MYSQL DATABASE FOR PRODUCTION*****)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")     

#Creates a secret key which is used by the forms (*****NEEDS TO BE CHANGED AND PUT IN AN ENVIRONMENT VARIABLE*****)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)        #Creates the database object

from application import routes
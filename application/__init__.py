from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

#Creates a local database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")     

#Creates a secret key which is used by the forms 
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)        #Creates the database object

from application import routes
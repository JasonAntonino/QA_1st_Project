from application import app, db                     #Imports the Flask app and Database objects
from application.models import Teams, Players       #Imports the tables of the database
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addTeam')
def addTeam():
    return render_template('addTeam.html')

@app.route('/addPlayer')
def addPlayer():
    return render_template('addPlayer.html')

from application import app                                             #Imports Flask app object from __init__.py
from flask import Flask, render_template, request                       #Flask imports
from flask_wtf import FlaskForm                                         #Imports form from flask_wtf
from wtforms import StringField, IntegerField, SelectField, SubmitField              #Imports used fields for the form
from wtforms.validators import DataRequired, Length, ValidationError    #Imports validators for the form

#Form for adding a new Team record
class TeamForm(FlaskForm):
    team_name = StringField('Team Name')        #Collects team name
    team_manager = StringField('Manager Name')  #Collects manager name
    team_location = StringField('Location')     #Collects location of team
    submit = SubmitField('Add Team')            #Submit button


#Form for adding a new Player record
class PlayerForm(FlaskForm):
    fk_team_id = SelectField('Team of the player', choices=[])      #Collects team id of player
    player_first_name = StringField('First Name')                   #Collects first name of player
    player_last_name = StringField('Last Name')                     #Collects last name of player
    player_age = IntegerField('Age')                                #Collects age of player
    submit = SubmitField('Add Player')                              #Submit button

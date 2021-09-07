from application import app                                             #Imports Flask app object from __init__.py
from flask import Flask, render_template, request                       #Flask imports
from flask_wtf import FlaskForm                                         #Imports form from flask_wtf
from wtforms import StringField, IntegerField, SelectField, SubmitField              #Imports used fields for the form
from wtforms.validators import DataRequired, Length, ValidationError    #Imports validators for the form
from application.models import Teams, Players

def validate_Team_name(self, field):
    allTeams = Teams.query.all()
    for team in allTeams:
        if field.data == team.team_name:
            raise ValidationError("The team already exists.")

#Form for adding a new Team record
class TeamForm(FlaskForm):
    team_name = StringField('Team Name', 
        validators=[DataRequired(), Length(min=1, max=50), validate_Team_name])   #Collects team name
    
    team_manager = StringField('Manager Name',
        validators=[DataRequired(), Length(min=1, max=120)])  #Collects manager name
    
    team_location = StringField('Location',
        validators=[DataRequired(), Length(min=1, max=200)])  #Collects location of team
    
    submit = SubmitField('Submit')                          #Submit button

#Form for selecting a team to update
class UpdateTeamForm(FlaskForm):
    team_name = SelectField('Select Team to update', choices=[],
        validators=[DataRequired()])

    submit = SubmitField('Edit Team')

#Form for selecting a team to delete
class DeleteTeamForm(FlaskForm):
    team_id = SelectField('Select Team to delete', choices=[],
        validators=[DataRequired()])

    submit = SubmitField('Delete Team')

#Form for adding a new Player record
class PlayerForm(FlaskForm):
    fk_team_id = SelectField('Team of the player', choices=[],
        validators=[DataRequired()])                            #Collects team id of player
    
    player_first_name = StringField('First Name',
        validators=[DataRequired(), Length(min=1, max=100)])    #Collects first name of player
    
    player_last_name = StringField('Last Name',
        validators=[DataRequired(), Length(min=1, max=100)])    #Collects last name of player
    
    player_age = IntegerField('Age',
        validators=[DataRequired()])                            #Collects age of player
        
    submit = SubmitField('Submit')                          #Submit button

#Form for selecting a player to update
class UpdatePlayerForm(FlaskForm):
    player_id = SelectField('Select player to update', choices=[],
        validators=[DataRequired()])

    submit = SubmitField('Edit Player')

#Form for selecting a player to delete
class DeletePlayerForm(FlaskForm):
    player_id = SelectField('Select player to delete', choices=[],
        validators=[DataRequired()])

    submit = SubmitField('Delete Player')

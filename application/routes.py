from application import app, db                     #Imports the Flask app and Database objects
from application.models import Teams, Players       #Imports the tables of the database
from flask import render_template, request
from application.forms import TeamForm, PlayerForm  #Imports the forms for adding a new team and player records

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/addTeam', methods=['GET', 'POST'])
def addTeam():
    form = TeamForm()               #Creating a new team form

    if request.method == 'POST':    #If a form is submitted (from html file)
        #Create a new Team record - Send data from form to database
        newTeam = Teams(
            team_name = form.team_name.data,
            team_manager = form.team_manager.data,
            team_location = form.team_location.data
        )

        db.session.add(newTeam)     #Stages newly created team record
        db.session.commit()         #Puts staged team record into the database

        message = f"You have added the team: {form.team_name.data}"

        return render_template('addTeam.html', form=form, message=message)
    
    return render_template('addTeam.html', form=form)



@app.route('/addPlayer', methods=['GET', 'POST'])
def addPlayer():
    form = PlayerForm()

    allTeams = Teams.query.all()    #Collects all team record within the database

    #Adds exisiting teams from database to choices of fk_team_id
    for team in allTeams:
        form.fk_team_id.choices.append(
            (team.id, f"{team.team_name}")      #Format: (team_id, label)
        )

    if request.method == 'POST':
        #Create a new Player record - data coming from form
        newPlayer = Players(
            fk_team_id = form.fk_team_id.data,
            player_first_name = form.player_first_name.data,
            player_last_name = form.player_last_name.data,
            player_age = form.player_age.data
        )

        db.session.add(newPlayer)
        db.session.commit()
        
        message = f"You have added the player: {form.player_first_name.data} {form.player_last_name.data}"

        return render_template('addPlayer.html', form=form, message=message)

    return render_template('addPlayer.html', form=form)

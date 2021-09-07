from application import app, db                     #Imports the Flask app and Database objects
from application.models import Teams, Players       #Imports the tables of the database
from flask import render_template, url_for, request, redirect, flash
from application.forms import TeamForm, PlayerForm, UpdateTeamForm, UpdatePlayerForm, DeletePlayerForm, DeleteTeamForm  #Imports the forms for adding a new team and player records

@app.route('/')
def home():
    allTeams = Teams.query.all()        #Gets all the teams - returns a list
    allPlayers = Players.query.all()    #Gets all the players - returns a list

    return render_template('home.html', allTeams=allTeams, allPlayers=allPlayers) #teamList=teamList)


@app.route('/addTeam', methods=['GET', 'POST'])
def addTeam():
    form = TeamForm()               #Creating a new team form

    if request.method == 'POST' and form.validate_on_submit():    #If a form is submitted (from html file)
        #Create a new Team record - Send data from form to database
        newTeam = Teams(
            team_name = form.team_name.data,
            team_manager = form.team_manager.data,
            team_location = form.team_location.data
        )

        db.session.add(newTeam)     #Stages newly created team record
        db.session.commit()         #Puts staged team record into the database

        message = f"You have added the team: {form.team_name.data}"

        flash(message)
        return redirect(url_for('addTeam'))
    
    return render_template('addTeam.html', form=form)


@app.route('/addPlayer', methods=['GET', 'POST'])
def addPlayer():
    form = PlayerForm()
    # form.validate_age(form.player_age)

    allTeams = Teams.query.all()    #Collects all team record within the database

    #Adds exisiting teams from database to choices of fk_team_id
    for team in allTeams:
        form.fk_team_id.choices.append(
            (team.id, f"{team.team_name}")      #Format: (team_id, label)
        )

    if request.method == 'POST' and form.validate_on_submit():
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

        flash(message)
        return redirect(url_for('addPlayer'))
    return render_template('addPlayer.html', form=form)


#First page shown when updating a Team's details
@app.route('/updateTeam', methods=['GET', 'POST'])
def updateTeam():
    form = UpdateTeamForm()         #Only cotains a select field which asks for which team to update

    allTeams = Teams.query.all()    #Collects all team record within the database
    
    #Adds exisiting teams from database to choices of team_name
    #The select field will display team names (not team id)
    for team in allTeams:
        form.team_name.choices.append(
            (team.team_name, f"{team.team_name}")      #Format: (team_name, label)
        )

    #If HTTP Request = POST and all validations are good:
    if request.method == 'POST' and form.validate_on_submit():
        #Gets the team record for the selected team
        chosenTeam = Teams.query.filter_by(team_name=form.team_name.data).first()
        #Retrieves the team name of the selected team
        chosenTeamName = chosenTeam.team_name

        #Upon form submission, user is redirected to a new page
        #The selected team's name is also passed in the URL (part of url_for())
        return redirect(url_for('updateTeamDetails', chosenTeamName=chosenTeamName))
    
    #If HTTP Request = GET or some validations are bad, render the same page
    return render_template('updateTeam.html', form=form)


@app.route('/updateTeam/<chosenTeamName>', methods=['GET', 'POST'])
def updateTeamDetails(chosenTeamName):
    form = TeamForm()      #This is the same form as the one used for adding a new team

    #Gets the team record based on the given team name from the URL
    chosenTeam = Teams.query.filter_by(team_name=chosenTeamName).first()

    #If HTTP Request = POST and all validations are good:
    if request.method == 'POST' and form.validate_on_submit():
        message = f"""Changes: 
            {chosenTeam.team_name} to {form.team_name.data}, 
            {chosenTeam.team_manager} to {form.team_manager.data}, 
            {chosenTeam.team_location} to {form.team_location.data}"""
        
        #Update the specific team record based on the user input on the form
        chosenTeam.team_name = form.team_name.data
        chosenTeam.team_manager = form.team_manager.data
        chosenTeam.team_location = form.team_location.data
        db.session.commit()

        flash(message)  #Displays the message in the destination page
        return redirect(url_for('updateTeam'))
    
    return render_template('updateTeamDetails.html', form=form)


@app.route('/updatePlayer', methods=['GET', 'POST'])
def updatePlayer():
    form = UpdatePlayerForm()
    allPlayers = Players.query.all()

    for player in allPlayers:
        #If current player's fk_team_id matches chosenteamid
        #Add player firstname and lastname to the choices in the form
        form.player_id.choices.append(
            (player.id, f"{player.player_first_name} {player.player_last_name}")
        )

    if request.method == 'POST' and form.validate_on_submit():
        chosenPlayerId = form.player_id.data
        return redirect(url_for('updatePlayerDetails', chosenPlayerId=chosenPlayerId))

    return render_template('updatePlayer.html', form=form)


@app.route('/updatePlayer/<chosenPlayerId>', methods=['GET', 'POST'])
def updatePlayerDetails(chosenPlayerId):
    form = PlayerForm()
    chosenPlayer = Players.query.get(int(chosenPlayerId))

    #Collects all team record within the database
    allTeams = Teams.query.all()    
    #Adds exisiting teams from database to choices of fk_team_id
    for team in allTeams:
        form.fk_team_id.choices.append(
            (team.id, f"{team.team_name}")      #Format: (team_id, label)
        )

    if request.method == 'POST' and form.validate_on_submit():
        message = f"""Changes: 
            {chosenPlayer.player_first_name} to {form.player_first_name.data}, 
            {chosenPlayer.player_last_name} to {form.player_last_name.data}, 
            {chosenPlayer.player_age} to {form.player_age.data}"""

        chosenPlayer.fk_team_id = form.fk_team_id.data
        chosenPlayer.player_first_name = form.player_first_name.data
        chosenPlayer.player_last_name = form.player_last_name.data
        chosenPlayer.player_age = form.player_age.data
        db.session.commit()

        flash(message)
        return redirect(url_for('updatePlayer'))

    return render_template('updatePlayerDetails.html', form=form)


@app.route('/deletePlayer', methods=['GET', 'POST'])
def deletePlayer():
    form = DeletePlayerForm()

    allPlayers = Players.query.all()

    for player in allPlayers:
        form.player_id.choices.append(
            (player.id, f"{player.player_first_name} {player.player_last_name}")
        )

    if request.method == 'POST' and form.validate_on_submit():
        chosenPlayerId = form.player_id.data
        playerToDelete = Players.query.get(chosenPlayerId)

        db.session.delete(playerToDelete)
        db.session.commit()

        message = f"Player {playerToDelete.player_first_name} {playerToDelete.player_last_name} has been deleted."
        flash(message)
        return redirect(url_for('deletePlayer'))

    return render_template('deletePlayer.html', form=form)


@app.route('/deleteTeam', methods=['GET', 'POST'])
def deleteTeam():
    form = DeleteTeamForm()

    allTeams = Teams.query.all()
    #Adds exisiting teams from database to choices of fk_team_id
    for team in allTeams:
        form.team_id.choices.append(
            (team.id, f"{team.team_name}")      #Format: (team_id, label)
        )

    if request.method == 'POST' and form.validate_on_submit():
        teamIdToDelete = form.team_id.data

        playersToDelete = Players.query.filter_by(fk_team_id=teamIdToDelete).all()

        #Deletes all the players associated with the team to delete
        for player in playersToDelete:
            db.session.delete(player)
            db.session.commit()
        

        teamToDelete = Teams.query.get(teamIdToDelete)
        db.session.delete(teamToDelete)
        db.session.commit()

        message = f"Team {teamToDelete.team_name} has been deleted."
        flash(message)

        return redirect(url_for('deleteTeam'))

    return render_template('deleteTeam.html', form=form)
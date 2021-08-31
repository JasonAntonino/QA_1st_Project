from application import app, db                     #Imports the Flask app and Database objects
from application.models import Teams, Players       #Imports the tables of the database

@app.route('/')
def home():
    #Creates a team named Manchester United
    manchesterUnited = Teams(
        team_name = "Manchester United",
        team_manager = "Ole Gunnar Solskjaer",
        team_location = "Manchester",
    )

    #Creates a player for Manchester United
    player1 = Players(
        fk_team_id = manchesterUnited.id,
        player_first_name = "Bruno",
        player_last_name = "Fernandes",
        player_age = 26
    )

    db.session.add(manchesterUnited)
    db.session.commit()

    print(manchesterUnited)
    print(player1)


    return "Added a new team and a player"

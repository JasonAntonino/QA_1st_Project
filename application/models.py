from application import db          #Imports the database object

#Teams Table
class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)                            #Primary Key
    team_name = db.Column(db.String(50), unique=True, nullable=False)       #Name VARCHAR(50) NOT NULL
    team_manager = db.Column(db.String(120), nullable=False)                #Manager VARCHAR(120) NOT NULL
    team_location = db.Column(db.String(200), nullable=False)               #Location VARCHAR(200) NOT NULL
    players = db.relationship('Players', backref='teams')

#Players Table
class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                        #Primary Key
    fk_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)       #Foreign Key - Teams table
    player_first_name = db.Column(db.String(100), nullable=False)                       #First name VARCHAR(100) NOT NULL
    player_last_name = db.Column(db.String(100), nullable=False)                        #Last name VARCHAR(100) NOT NULL
    player_age = db.Column(db.Integer, nullable=False)                                  #Age INT NOT NULL
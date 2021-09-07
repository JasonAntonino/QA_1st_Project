from flask_testing import TestCase              #Used for setting conditions of Flask application during testing
from application import app, db                 #Imports the Flask app and database objects
from application.models import Teams, Players   #Imports the database models
from flask import url_for

class TestBase(TestCase):
    #Sets up the Flask app configurations
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///testDB.db',
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app


    #Function is run before each test
    def setUp(self):
        db.create_all()     #Creates all the tables

        #Creates a new Team record
        newTeam = Teams(
            team_name = "Manchester United", 
            team_manager = "Ole Gunnar Solskjaer",
            team_location = "Manchester")
        
        #Adds new Team record into the database
        db.session.add(newTeam)
        db.session.commit()

        newPlayer = Players(
            fk_team_id = 1,
            player_first_name = "Bruno",
            player_last_name = "Fernandes",
            player_age = "26"
        )

        #Adds new Player record into the database
        db.session.add(newPlayer)
        db.session.commit()


    #Function is run after each test
    def tearDown(self):
        db.session.remove()     #Removes all records in the database
        db.drop_all()           #Drops all of the tables in the database


#Testing: Loading each page in the application
class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_addTeam_get(self):
        response = self.client.get(url_for('addTeam'))
        self.assertEqual(response.status_code, 200)

    def test_addPlayer_get(self):
        response = self.client.get(url_for('addPlayer'))
        self.assertEqual(response.status_code, 200)

    def test_updateTeam_get(self):
        response = self.client.get(url_for('updateTeam'))
        self.assertEqual(response.status_code, 200)

    def test_updatePlayer_get(self):
        response = self.client.get(url_for('updatePlayer'))
        self.assertEqual(response.status_code, 200)

    def test_deletePlayer_get(self):
        response = self.client.get(url_for('deletePlayer'))
        self.assertEqual(response.status_code, 200)

    def test_deleteTeam_get(self):
        response = self.client.get(url_for('deleteTeam'))
        self.assertEqual(response.status_code, 200)


#Testing: CREATE Operation of the application
class TestCreate(TestBase):

    #Testing: Adding a new Team Record
    def test_add_Team(self):
        response = self.client.post(        #Creating a post request
            url_for('addTeam'),             #Post request going to addTeam route function
            
            #Adding a new Team record
            data = dict(
                team_name = "Chelsea",
                team_manager = "Tomas Tuchel",
                team_location = "London"
            ),
            follow_redirects=True
        )
        #Checking that new Team record has been added to the database
        assert Teams.query.filter_by(team_name="Chelsea").first().id == 2


    #Testing: Adding a new Player Record
    def test_add_Player(self):
        response = self.client.post(    #Creating a post request
            url_for('addPlayer'),       #Post request going to addPlayer route function
            
            #Adding a new Player record
            data = dict(
                fk_team_id = 1,
                player_first_name = "Kai",
                player_last_name = "Havertz",
                player_age = 22
            ),
            follow_redirects=True
        )
        #Checking that new Team record has been added to the database
        player = Players.query.get(2)
        assert player.player_first_name == "Kai"
        assert player.player_last_name == "Havertz"
        assert player.player_age == 22


#Testing: READ Operation of the application
class TestRead(TestBase):

    #Testing: Reading a Team record from the database
    def test_read_Team(self):
        teamRetrieved = Teams.query.first()
        assert teamRetrieved.team_name == "Manchester United"
        assert teamRetrieved.team_manager == "Ole Gunnar Solskjaer"
        assert teamRetrieved.team_location == "Manchester"

    #Testing: Reading a Player record from the database
    def test_read_Player(self):
        playerRetrieved = Players.query.first()
        assert playerRetrieved.player_first_name == "Bruno"
        assert playerRetrieved.player_last_name == "Fernandes"
        assert playerRetrieved.player_age == 26


# Testing: UPDATE Operation of the application
class TestUpdate(TestBase):
    #Testing: Updating a Team record
    def test_update_Team(self):
        response = self.client.post(
            url_for('updateTeam'),
            data = dict(
                team_name = "Manchester United"
            ),
            follow_redirects = True
        )

        response2 = self.client.post(
            url_for('updateTeamDetails', chosenTeamName="Manchester United"),
            data = dict(
                team_name = "New Manchester United",
                team_manager = "New Manager",
                team_location = "New Manchester"
            ),
            follow_redirects = True
        )

        self.assertIn(b"Update Team", response.data)
        self.assertEqual(response.status_code, 200)


    #Testing: Updating a Player record
    def test_update_Player(self):
        response = self.client.post(
            url_for('updatePlayer'),
            data = dict(
                player_id=1
            ),
            follow_redirects = True
        )

        response = self.client.post(
            url_for('updatePlayerDetails', chosenPlayerId=1),
            data = dict(
                fk_team_id = 1,
                player_first_name = "New Bruno",
                player_last_name = "New Fernandes",
                player_age = 35
            ),
            follow_redirects = True
        )

        self.assertIn(b"Update Player", response.data)
        self.assertEqual(response.status_code, 200)


#Testing: DELETE Operation of the application
class TestDelete(TestBase):
    #Testing: Deleting a Team record
    def test_delete_Team(self):
        response = self.client.post(
            url_for('deleteTeam'),
            data = dict(
                team_id = 1
            ),
            follow_redirects=True
        )
        self.assertIn(b"Delete a Team", response.data)
        self.assertEqual(response.status_code, 200)
        
        
    #Testing: Deleting a Player record
    def test_delete_Player(self):
        response = self.client.post(
            url_for('deletePlayer'),
            data = dict(
                player_id = 1
            ),
            follow_redirects=True
        )
        self.assertIn(b"Delete a Player", response.data)
        self.assertEqual(response.status_code, 200)


#Testing: ValidationError raises from forms
class TestValidationError(TestBase):
    #Testing: Adding same team name into the database
    def test_unique_team_name(self):
        response = self.client.post(        #Creating a post request
            url_for('addTeam'),             #Post request going to addTeam route function
            
            #Adding a new Team record with the same team name as existing data in database
            data = dict(
                team_name = "Manchester United",    #Manchester United already exists in the database
                team_manager = "Tomas Tuchel",
                team_location = "London"
            ),
            follow_redirects=True
        )
        #Checks that a ValidationError has been raised
        assert "The team already exists."
from selenium import webdriver  
from flask_testing import LiveServerTestCase    #Allows to create a live instance of the application
from application import app, db
from application.models import Teams, Players
from urllib.request import urlopen

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///testDB.db',
            LIVESERVER_PORT = self.TEST_PORT,
            DEBUG=True,
            TESTING = True
        )
        return app

    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')   #Prevents GUI from appearing

        self.driver = webdriver.Chrome(options=chrome_options)

        db.create_all()

        #Creates a new Team and adds to database
        newTeam = Teams(
            team_name = "Arsenal",
            team_manager = "Mikel Arteta",
            team_location = "London"
        )
        db.session.add(newTeam)
        db.session.commit()

        #Creates a new Player record and adds to database
        newPlayer = Players(
            fk_team_id = 1,
            player_first_name = "Lionel",
            player_last_name = "Messi",
            player_age = 34
        )
        db.session.add(newPlayer)
        db.session.commit()

        self.driver.get(f'http://localhost:{self.TEST_PORT}')
        
    def tearDown(self):
        self.driver.quit()
        db.drop_all()

    def test_server_is_up_and_running(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}')
        self.assertEqual(response.code, 200)


class TestCreate(TestBase):
    def test_create_Team(self):
        # self.driver.get(f'http://localhost:{self.TEST_PORT}/addTeam')
        self.driver.find_element_by_xpath("/html/body/div[1]/a[2]").click()

        teamNameField = self.driver.find_element_by_xpath('//*[@id="team_name"]')
        teamNameField.send_keys("Liverpool FC")

        teamManagerField = self.driver.find_element_by_xpath('//*[@id="team_manager"]')        
        teamManagerField.send_keys("Jurgen Klopp")

        teamLocationField = self.driver.find_element_by_xpath('//*[@id="team_location"]')
        teamLocationField.send_keys("Liverpool")

        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        teams = Teams.query.all()
        self.assertEqual(Teams.query.count(), 2)

    
    def test_create_Player(self):
        #Click "Add a Player" in the navigation bar
        self.driver.find_element_by_xpath('/html/body/div[1]/a[3]').click()

        #Give form details
        teamNameField = self.driver.find_element_by_xpath('//*[@id="fk_team_id"]')

        firstNameField = self.driver.find_element_by_xpath('//*[@id="player_first_name"]')
        firstNameField.send_keys("Ben")

        lastNameField = self.driver.find_element_by_xpath('//*[@id="player_last_name"]')
        lastNameField.send_keys("White")

        ageField = self.driver.find_element_by_xpath('//*[@id="player_age"]')
        ageField.send_keys(23)

        #Click the submit button
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        #Assert checks: 2 == 2 (2 records in the Players table)
        self.assertEqual(Players.query.count(), 2)


class TestUpdate(TestBase):
    def test_update_Team(self):
        #Click "Update Team details" in the navigation bar
        self.driver.find_element_by_xpath('/html/body/div[1]/a[4]').click()

        #Give form details - 1st Page
        teamToUpdate = self.driver.find_element_by_xpath('//*[@id="team_name"]')

        #Click submit button - 1st Page
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        #Give form details - 2nd page
        teamNameField = self.driver.find_element_by_xpath('//*[@id="team_name"]')
        teamNameField.send_keys("Updated Arsenal")

        teamManagerField = self.driver.find_element_by_xpath('//*[@id="team_manager"]')        
        teamManagerField.send_keys("Updated Mikel Arteta")

        teamLocationField = self.driver.find_element_by_xpath('//*[@id="team_location"]')
        teamLocationField.send_keys("Updated London")

        #Click submit button - 2nd Page
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        team = Teams.query.first()  #Collects only team in database
        
        #Asserts check: team details have been updated
        self.assertEqual(team.team_name, "Updated Arsenal")
        self.assertEqual(team.team_manager, "Updated Mikel Arteta")
        self.assertEqual(team.team_location, "Updated London")

    def test_update_Player(self):
        #Click "Update Player details" in the navigation bar
        self.driver.find_element_by_xpath('/html/body/div[1]/a[5]').click()

        #Give form details - 1st Page
        playerToUpdate = self.driver.find_element_by_xpath('//*[@id="player_id"]')

        #Click submit button - 1st Page
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        #Give form details - 2nd Page
        teamNameField = self.driver.find_element_by_xpath('//*[@id="fk_team_id"]')

        firstNameField = self.driver.find_element_by_xpath('//*[@id="player_first_name"]')
        firstNameField.send_keys("Updated Lionel")

        lastNameField = self.driver.find_element_by_xpath('//*[@id="player_last_name"]')
        lastNameField.send_keys("Updated Messi")

        ageField = self.driver.find_element_by_xpath('//*[@id="player_age"]')
        ageField.send_keys(23)

        #Click the submit button - 2nd Page
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        player = Players.query.first()  #Collects only player in database

        #Asserts check: player details have been updated
        self.assertEqual(player.player_first_name, "Updated Lionel")
        self.assertEqual(player.player_last_name, "Updated Messi")
        self.assertEqual(player.player_age, 23)


class TestDelete(TestBase):
    def test_delete_Team(self):
        #Click "Delete a Team" in the navigation bar
        self.driver.find_element_by_xpath('/html/body/div[1]/a[7]').click()

        #Give form details
        teamToDelete = self.driver.find_element_by_xpath('//*[@id="team_id"]')

        #Click the submit button
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        #Assert checks: 0 == 0 (no more team record in database)
        self.assertEqual(Teams.query.count(), 0)

    
    def test_delete_Player(self):
        #Click "Delete a Player" in the navigation bar
        self.driver.find_element_by_xpath('/html/body/div[1]/a[6]').click()

        #Give form details
        playerToDelete = self.driver.find_element_by_xpath('//*[@id="player_id"]')

        #Click the submit button
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        #Assert checks: 0 == 0 (no more player record in database)
        self.assertEqual(Players.query.count(), 0)
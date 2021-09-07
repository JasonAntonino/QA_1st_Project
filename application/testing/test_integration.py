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
            # WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')   #Prevents GUI from appearing

        self.driver = webdriver.Chrome(options=chrome_options)

        db.create_all()
        self.driver.get(f'http://localhost:{self.TEST_PORT}')
    
    def tearDown(self):
        self.driver.quit()
        db.drop_all()

    def test_server_is_up_and_running(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}')
        self.assertEqual(response.code, 200)


class TestCreate(TestBase):
    def test_create_Team(self):
        self.driver.get(f'http://localhost:{self.TEST_PORT}/addTeam')

        print("works 1")

        teamNameField = self.driver.find_element_by_xpath("/html/body/div[2]/form/input[2]")
        teamNameField.send_keys("Liverpool FC")

        print("works 2")

        teamManagerField = self.driver.find_element_by_xpath("/html/body/div[2]/form/input[3]")
        teamManagerField.send_keys("Jurgen Klopp")

        print("works 3")

        teamLocationField = self.driver.find_element_by_xpath("/html/body/div[2]/form/input[4]")
        teamLocationField.send_keys("Liverpool")

        print("works 4")

        self.driver.find_element_by_xpath("/html/body/div[2]/form/input[5]").click()

        print("works 5")

        teams = Teams.query.all()
        self.assertEqual(len(teams), 1)


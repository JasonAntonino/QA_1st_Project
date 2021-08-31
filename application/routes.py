from application import app, db     #Imports the Flask app and Database objects

@app.route('/')
def home():
    return "This is the home page"

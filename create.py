from application import db          #Imports the database object

db.drop_all()
db.create_all()
# DevOps Core Fundamental Project

## Project Objective
The main objective of this project is to create a CRUD application which incorporates all the supporting tools and technologies covered during training:

* Project Management
* Python Fundamentals
* Python Testing
* Git
* Basic Linux
* Python Web Development
* Continuous Integration
* Cloud Fundamentals
* Databases


## Database Design
For the database of the application, there are two main tables that are involved, as shown in the Entity Relationship Diagram below:

![Entity Relationships Diagram](images/entity_relationships_diagram.png)

The Teams table has 4 total fields, with team_id being the Primary Key. As for the Player table, there are a total of 5 fields, where player_id is the Primary Key. In addition to this, the Player table has a Foreign Key named fk_team_id.
  
These two tables have a One-to-Many relationship, which is denoted by the link between the two tables shown in the diagram above. This relationship means that one team can have zero to many players, whilst one player can only ever have one team at any given time. This is vital as it ensures that the database accurately represents what typically occurs in the real world.


## Risk Assessment
This section looks into the possible risks that may arise during the development of the application.

![Risk assessment table](images/risk_assessment.png)


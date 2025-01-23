# casting-agency

Udacity Final Project

This project is the final project of the Udacity Full Stack Developer Nano Degree Program. The goal of this project is to deploy a Flask application with Render Cloud/PostgreSQL and enable Role Based Authentication and roles-based access control (RBAC) with Auth0 (third-party authentication systems).

I have implemented the Casting Agency model of a company that assigns movies to actors. There are three roles within the company of Assistant, Director and Producer.

Getting Started
Installing Dependencies
Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

Virtual Environment
I recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organized. Instructions for setting up a virtual environment for the platform can be found in the python docs.

PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by running:

$ pip install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.

Running the server
first ensure you are working using your created virtual environment.

To run the server, execute:

$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run

Environment variables are set in the .env file.

Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

Setting the FLASK_APP variable to app.py directs flask to use the this file to find the application.

Models:
Movies model defined with attributes title, release date, genre, and actor id.
Actors model defined with attributes name and age.
You can find the models in models.py file. Local Postgres DATABASE details are available in .env file for reference.

Endpoints:
All below Endpoints have been created, please refer app.py file.
GET /actors & /movies
DELETE /actors/<int:id> & /movies/<int:id>
POST /actors & /movies
PATCH /actors/<int:id> & /movies/<int:id>

Auth0 Setup:
AUTH0_DOMAIN, ALGORITHMS and API_AUDIENCE are all available in the .env file for reference. Json Web Tokens: You can find JWTs for each role in the .env file to run the app locally.

Roles: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

Casting Assistant - Can get a list of movies an actors and also get by the ids of each.
Casting Director - All permissions a Casting Assistant has and is able to add and patch both actors and movies' list.
Executive Producer - All permissions a Casting Director has and can delete movies and actors from the database.

Deployment Details:
App is deployed to Heroku.
Heroku Postgres DATABASE details are available in setup.sh file for reference.
Use the above stated endpoints and append to this link above to execute the app either thru CURL or Postman. For example:

$ curl -X GET https://casting-agency-dynl.onrender.com/actors?page=1
$ curl -X POST https://casting-agency-dynl.onrender.com/actors
$ curl -X PATCH https://casting-agency-dynl.onrender.com/actors/1
$ curl -X DELETE https://casting-agency-dynl.onrender.com/actors/1

Follow the same pattern to hit the /movies endpoints too.

Testing:
We can run our entire test case by running the following command at command line:
$ python test_app.py

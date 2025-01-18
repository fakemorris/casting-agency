import json
import os
from flask import Flask, request, jsonify, _request_ctx_stack
from functools import wraps
import requests
from flask_sqlalchemy import SQLAlchemy
from models import db, Actor, Movie
from urllib.request import urlopen
from flask_cors import CORS
from flask_migrate import Migrate
from auth import requires_auth, AuthError
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Get all movies - GET method
@app.route("/movies", methods=["GET"])
@requires_auth('read:movies')
def get_movies():
    """
    Retrieves a list of all movies from the database.
    """
    movies = Movie.query.all()
    if not movies:
        return jsonify({
            "success": False,
            "message": "No movies found."
        }), 404

    return jsonify([movie.to_dict() for movie in movies])

# Get a specific movie by ID - GET method
@app.route("/movies/<int:movie_id>", methods=["GET"])
@requires_auth('read:movies')
def get_movie(movie_id):
    """
    Retrieves a specific movie by its ID.
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({
            "success": False,
            "message": "Movie not found."
        }), 404

    return jsonify(movie.to_dict())

# Add a new movie - POST method
@app.route("/movies", methods=["POST"])
@requires_auth('add:movies')
def add_movie():
    """
    Adds a new movie to the database.
    """
    data = request.json
    movie_title = data.get("title")
    movie_release_year = data.get("release_year")

    if not movie_title or not movie_release_year:
        return jsonify({
            "success": False,
            "message": "Title and Release Year are required."
        }), 400

    new_movie = Movie(title=movie_title, release_year=movie_release_year)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify(new_movie.to_dict()), 201

# Update an existing movie - PATCH method
@app.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth('patch:movies')
def update_movie(movie_id):
    """
    Updates an existing movie's details.
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({
            "success": False,
            "message": "Movie not found."
        }), 404

    data = request.json
    movie_title = data.get("title")
    movie_release_year = data.get("release_year")

    if movie_title:
        movie.title = movie_title
    if movie_release_year:
        movie.release_year = movie_release_year

    db.session.commit()

    return jsonify(movie.to_dict())

# Delete a movie - DELETE method
@app.route("/movies/<int:movie_id>", methods=["DELETE"])
@requires_auth('delete:movies')
def delete_movie(movie_id):
    """
    Deletes a movie by its ID from the database.
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({
            "success": False,
            "message": "Movie not found."
        }), 404

    db.session.delete(movie)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Movie with ID {movie_id} has been deleted."
    })

# Get all actors - GET method
@app.route("/actors", methods=["GET"])
@requires_auth('read:actors')
def get_actors():
    """
    Retrieves a list of all actors from the database.
    """
    actors = Actor.query.all()
    if not actors:
        return jsonify({
            "success": False,
            "message": "No actors found."
        }), 404

    return jsonify([actor.to_dict() for actor in actors])

# Get a specific actor by ID - GET method
@app.route("/actors/<int:actor_id>", methods=["GET"])
@requires_auth('read:actors')
def get_actor(actor_id):
    """
    Retrieves a specific actor by their ID.
    """
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({
            "success": False,
            "message": "Actor not found."
        }), 404

    return jsonify(actor.to_dict())

# Add a new actor - POST method
@app.route("/actors", methods=["POST"])
@requires_auth('add:actors')
def add_actor():
    """
    Adds a new actor to the database.
    """
    data = request.json
    actor_name = data.get("name")
    actor_age = data.get("age")

    if not actor_name or not actor_age:
        return jsonify({
            "success": False,
            "message": "Name and Age are required."
        }), 400

    new_actor = Actor(name=actor_name, age=actor_age)
    db.session.add(new_actor)
    db.session.commit()

    return jsonify(new_actor.to_dict()), 201

# Update an actor - PATCH method
@app.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth('patch:actors')
def update_actor(actor_id):
    """
    Updates an existing actor's details.
    """
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({
            "success": False,
            "message": "Actor not found."
        }), 404

    data = request.json
    actor_name = data.get("name")
    actor_age = data.get("age")

    if actor_name:
        actor.name = actor_name
    if actor_age:
        actor.age = actor_age

    db.session.commit()

    return jsonify(actor.to_dict())

# Delete an actor - DELETE method
@app.route("/actors/<int:movie_id>", methods=["DELETE"])
@requires_auth('delete:actors')
def delete_actor(actor_id):
    """
    Deletes an actor by its ID from the database.
    """
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({
            "success": False,
            "message": "Actor not found."
        }), 404

    db.session.delete(actor)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Movie with ID {actor_id} has been deleted."
    })


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

@app.errorhandler(404)
def resource_not_found(error):
    print(f"Error occurred: {str(error)}")
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
    
@app.errorhandler(403)
def notFound(error):
    print(f"Error occurred: {str(error)}")
    return jsonify({
        "success": False,
        "error": 403,
        "message": "permission not found"
    }), 403
    
@app.errorhandler(Exception)
def handle_general_error(error):
    print(f"Error occurred: {str(error)}")
    return jsonify({
        'success': False,
        'message': 'An error occurred while processing the request.'
    }), 500

if __name__ == "__main__":
    app.run(debug=True)
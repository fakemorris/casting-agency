from datetime import datetime
import json
from sqlalchemy import create_engine
import os
from flask import Flask, request, jsonify, _request_ctx_stack
from functools import wraps
import requests
from flask_sqlalchemy import SQLAlchemy
from urllib.request import urlopen
from flask_cors import CORS
from flask_migrate import Migrate
from auth import requires_auth, AuthError
from dotenv import load_dotenv
from models import db, Movie, Actor

load_dotenv()

migrate = Migrate()

def create_app():
    """Factory function to create and configure the Flask app."""
    print("Creating the app...")
    # Initialize the Flask app
    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing

    # Load environment variables
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('RENDER_DATABASE_URL')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('LOCAL_DATABASE_URL')

    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy and Migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def home():
        return 'Welcome to the Casting Agency!'

    @app.route("/movies", methods=["GET"])
    @requires_auth('read:movies')
    def get_movies():
        """Retrieves a list of all movies from the database."""
        movies = Movie.query.all()
        if not movies:
            return jsonify({
                "success": False,
                "message": "No movies found."
            }), 404

        return jsonify([movie.to_dict() for movie in movies])

    @app.route("/movies/<int:movie_id>", methods=["GET"])
    @requires_auth('read:movies')
    def get_movie(movie_id):
        """Retrieves a specific movie by its ID."""
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({
                "success": False,
                "message": "Movie not found."
            }), 404

        return jsonify(movie.to_dict())

    @app.route("/movies", methods=["POST"])
    @requires_auth('add:movies')  # Uncomment if you're implementing authentication
    def add_movie():
        """Adds a new movie to the database."""
        data = request.json
    
        movie_title = data.get("title")
        release_date_str = data.get("release_date")
        genre = data.get("genre")
        actor_id = data.get("actor_id")

        if not movie_title or not release_date_str or not genre or not actor_id:
            return jsonify({
                "success": False,
                "message": "Title, Release Date, Genre, and Actor ID are required."
            }), 400

        # Check if the actor exists
        actor = Actor.query.get(actor_id)
        if not actor:
            return jsonify({
                "success": False,
                "message": "Actor not found."
            }), 404

        # Try parsing the date and handle potential errors
        try:
            release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Invalid date format. Please use YYYY-MM-DD."
            }), 400

        try:
            # Create the new movie and add it to the database
            new_movie = Movie(
                title=movie_title,
                release_date=release_date,
                genre=genre,
                actor_id=actor_id
            )

            db.session.add(new_movie)
            db.session.commit()

            # Return the newly created movie as a JSON response
            return jsonify(new_movie.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding movie: {str(e)}")  # Log the error for debugging
            return jsonify({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }), 500

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth('patch:movies')  # Uncomment if using authentication
    def update_movie(movie_id):
        """Updates an existing movie's details."""
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({
                "success": False,
                "message": "Movie not found."
        }), 404

        data = request.json
        movie_title = data.get("title")
        release_date_str = data.get("release_date")
        genre = data.get("genre")
        actor_id = data.get("actor_id")

        if release_date_str:
            try:
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
                movie.release_date = release_date
            except ValueError:
                return jsonify({
                    "success": False,
                    "message": "Invalid release date format. Expected format: YYYY-MM-DD."
                }), 400

        if movie_title:
            if not movie_title.strip():
                return jsonify({
                    "success": False,
                    "message": "Title cannot be empty."
                }), 400
            movie.title = movie_title

        if genre:
            movie.genre = genre

        if actor_id:
            actor = Actor.query.get(actor_id)
            if not actor:
                return jsonify({
                    "success": False,
                    "message": "Actor not found."
                }), 404
            movie.actor_id = actor_id

        db.session.commit()

        return jsonify(movie.to_dict())

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        """Deletes a movie by its ID from the database."""
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

    @app.route("/actors", methods=["GET"])
    @requires_auth('read:actors')
    def get_actors():
        """Retrieves a list of all actors from the database."""
        actors = Actor.query.all()
        if not actors:
            return jsonify({
                "success": False,
                "message": "No actors found."
            }), 404

        return jsonify([actor.to_dict() for actor in actors])

    @app.route("/actors/<int:actor_id>", methods=["GET"])
    @requires_auth('read:actors')
    def get_actor(actor_id):
        """Retrieves a specific actor by their ID."""
        actor = Actor.query.get(actor_id)
        if not actor:
            return jsonify({
                "success": False,
                "message": "Actor not found."
            }), 404

        return jsonify(actor.to_dict())

    @app.route("/actors", methods=["POST"])
    @requires_auth('add:actors')
    def add_actor():
        """Adds a new actor to the database."""
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

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
        """Updates an existing actor's details."""
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

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        """Deletes an actor by its ID from the database."""
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
            "message": f"Actor with ID {actor_id} has been deleted."
        })

    # Error handlers
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
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(403)
    def notFound(error):
        print(f"Error occurred: {str(error)}")
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Permission not found"
        }), 403

    @app.errorhandler(Exception)
    def handle_general_error(error):
        print(f"Error occurred: {str(error)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing the request.'
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request, check the request format and data.'
        }), 400
    
    @app.route('/tabs/user-page')
    def user_page():
        access_token = request.args.get('access_token')
    
        if access_token:
            return 'Login was successful!'
        else:
            return 'Login failed. No access token found.'
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

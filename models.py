from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

# Initialize the database and migrations
db = SQLAlchemy()

# Actor model
class Actor(db.Model):
    __tablename__ = 'actors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    movies = db.relationship('Movie', backref='actor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Actor {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }

# Movie model
class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    actor = db.relationship('Actor', backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f'<Movie {self.title}>'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%d"),
            'genre': self.genre,
            'actor_id': self.actor_id,
            'actor': self.actor.to_dict()
        }
import pytest
import os
from app import app, db
from models import Actor, Movie
from dotenv import load_dotenv

load_dotenv()

# Fixture to initialize the app and database
@pytest.fixture
def client():
    database_url = os.getenv('LOCAL_DATABASE_URL')
    print(f"Using database URL: {database_url}")

    # Ensure app is created properly with context
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up the database before each test
    with app.app_context():
        db.create_all()  # Create tables

    # Use test client to make requests
    with app.test_client() as client:
        yield client

    # Tear down the database after each test
    with app.app_context():
        db.session.remove()
        db.drop_all()  # Drop tables after test


def test_get_actors(client):
    """Test the GET /actors route."""
    actor = Actor(name="Otm Shank", age=30)
    db.session.add(actor)
    db.session.commit()

    response = client.get('/actors')

    assert response.status_code == 200

    actors = json.loads(response.data)
    assert any(actor['name'] == "Otm Shank" for actor in actors)
    
# Test GET /actors when no actors exist
def test_get_actors_empty(client):
    response = client.get('/actors')
    assert response.status_code == 404
    assert b"No actors found." in response.data


# Test POST /add_actor route
def test_add_actor(client):
    """Test the POST /add_actor route."""
    new_actor = {
        "name": "Otm Shank",
        "age": 25
    }

    response = client.post('/add_actor', json=new_actor)

    assert response.status_code == 201

    actor = Actor.query.filter_by(name="Otm Shank").first()
    assert actor is not None
    assert actor.age == 25

# Test POST /add_actor with missing fields
def test_add_actor_missing_fields(client):
    response = client.post('/add_actor', json={"name": "Otm"})
    assert response.status_code == 400
    assert b"Name and Age are required." in response.data

def test_update_actor(client):
    """Test the PATCH /actors/<id> route."""
    actor = Actor(name="Otm Shank", age=40)
    db.session.add(actor)
    db.session.commit()

    updated_data = {
        "name": "Otm Shank",
        "age": 45
    }

    response = client.patch(f'/actors/{actor.id}', json=updated_data)

    assert response.status_code == 200

    updated_actor = Actor.query.get(actor.id)
    assert updated_actor.name == "Updated Actor"
    assert updated_actor.age == 45

# Test DELETE /actors/<id> route
def test_delete_actor(client):
    """Test the DELETE /actors/<id> route."""
    actor = Actor(name="Otm Shank", age=50)
    db.session.add(actor)
    db.session.commit()

    response = client.delete(f'/actors/{actor.id}')

    assert response.status_code == 200

    deleted_actor = Actor.query.get(actor.id)
    assert deleted_actor is None
    
# Test POST /movies route with missing fields
def test_add_movie_missing_fields(client):
    """Test the POST /movies route when required fields are missing."""
    new_movie = {
        "title": "Dial M for Muderousness",
        "release_year": 2021
        # Missing 'genre' and 'actor_id'
    }

    response = client.post('/movies', json=new_movie)

    assert response.status_code == 400
    assert b"Missing required fields" in response.data

# Test POST /movies route with non-existing actor_id
def test_add_movie_non_existing_actor(client):
    """Test the POST /movies route when the actor_id does not exist."""
    new_movie = {
        "title": "Dial M for Muderousness",
        "release_year": 2021,
        "genre": "Drama",
        "actor_id": 9999  # Non-existing actor_id
    }

    response = client.post('/movies', json=new_movie)

    assert response.status_code == 404
    assert b"Actor with the provided actor_id does not exist" in response.data

# Test PATCH /movies/<id> route with non-existing movie
def test_update_non_existing_movie(client):
    """Test the PATCH /movies/<id> route when the movie does not exist."""
    updated_data = {
        "title": "Dial M for Muderousness",
        "release_year": 2022,
        "genre": "Comedy"
    }

    response = client.patch('/movies/9999', json=updated_data)

    assert response.status_code == 404
    assert b"Movie not found" in response.data

# Test DELETE /movies/<id> route with non-existing movie
def test_delete_non_existing_movie(client):
    """Test the DELETE /movies/<id> route when the movie does not exist."""
    
    response = client.delete('/movies/9999')

    assert response.status_code == 404
    assert b"Movie not found" in response.data
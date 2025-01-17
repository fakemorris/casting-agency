import unittest
import os
import json
from app import create_app, db
from models import Actor, Movie
from dotenv import load_dotenv

load_dotenv()

# Set environment variables
assistant_token = os.environ.get('ASSISTANT_TOKEN')
director_token = os.environ.get('DIRECTOR_TOKEN')
producer_token = os.environ.get('PRODUCER_TOKEN')

class MainTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests."""
        cls.database_url = os.getenv('LOCAL_DATABASE_URL')
        print(f"Using database URL: {cls.database_url}")
        
        cls.app = create_app()
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = cls.database_url
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.testing = True
        
        # Set up the Flask app context
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    def setUp(self):
        """Runs before every test."""
        # Create all tables before each test
        db.create_all()

        # Set up the test client
        self.client = self.app.test_client()

    def tearDown(self):
        """Runs after every test."""
        # Remove the session and drop all tables after each test
        db.session.remove()
        db.drop_all()

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests."""
        cls.app_context.pop()

    def test_get_actors(self):
        """Test the GET /actors route."""
        actor = Actor(name="Otm Shank", age=30)
        db.session.add(actor)
        db.session.commit()

        response = self.client.get('/actors')

        self.assertEqual(response.status_code, 200)

        actors = json.loads(response.data)
        self.assertTrue(any(actor['name'] == "Otm Shank" for actor in actors))
    
    def test_get_actors_empty(self):
        """Test GET /actors when no actors exist."""
        response = self.client.get('/actors')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_actor_exists(self):
        """Test getting an actor that exists in the database."""
        actor = Actor(name="Test Actor", age=30)
        db.session.add(actor)
        db.session.commit()

        response = self.client.get('/actors/1', headers={'Authorization': f'Bearer {assistant_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], "Test Actor")

    def test_get_actor_not_found(self):
        """Test getting an actor that does not exist."""
        response = self.client.get('/actors/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Actor not found.")

    def test_get_actor_unauthorized(self):
        """Test unauthorized access to the endpoint."""
        response = self.client.get('/actors/1', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Unauthorized')

    def test_add_actor(self):
        """Test the POST /actors route."""
        new_actor = {
            "name": "Otm Shank",
            "age": 25
        }

        response = self.client.post('/actors', json=new_actor, headers={'Authorization': f'Bearer {director_token}'})

        self.assertEqual(response.status_code, 201)

        actor = Actor.query.filter_by(name="Otm Shank").first()
        self.assertIsNotNone(actor)
        self.assertEqual(actor.age, 25)

    def test_add_actor_missing_fields(self):
        """Test POST /actors route with missing fields."""
        response = self.client.post('/add_actor', json={"name": "Otm"}, headers={'Authorization': f'Bearer {director_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Name and Age are required.", response.data)

    def test_update_actor(self):
        """Test the PATCH /actors/<id> route."""
        actor = Actor(name="Otm Shank", age=40)
        db.session.add(actor)
        db.session.commit()

        updated_data = {
            "name": "Otm Shank",
            "age": 45
        }

        response = self.client.patch(f'/actors/{actor.id}', json=updated_data, headers={'Authorization': f'Bearer {director_token}'})

        self.assertEqual(response.status_code, 200)

        updated_actor = Actor.query.get(actor.id)
        self.assertEqual(updated_actor.name, "Otm Shank")
        self.assertEqual(updated_actor.age, 45)

    def test_delete_actor(self):
        """Test the DELETE /actors/<id> route."""
        actor = Actor(name="Otm Shank", age=50)
        db.session.add(actor)
        db.session.commit()

        response = self.client.delete(f'/actors/{actor.id}', headers={'Authorization': f'Bearer {producer_token}'})

        self.assertEqual(response.status_code, 200)

        deleted_actor = Actor.query.get(actor.id)
        self.assertIsNone(deleted_actor)

    def test_add_movie_missing_fields(self):
        """Test POST /movies with missing fields."""
        new_movie = {
            "title": "Dial M for Murderousness",
            "release_year": 2021
        }

        response = self.client.post('/movies', json=new_movie, headers={'Authorization': f'Bearer {director_token}'})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

    def test_add_movie_non_existing_actor(self):
        """Test POST /movies with non-existing actor_id."""
        new_movie = {
            "title": "Dial M for Murderousness",
            "release_year": 2021,
            "genre": "Drama",
            "actor_id": 9999  # Non-existing actor_id
        }

        response = self.client.post('/movies', json=new_movie, headers={'Authorization': f'Bearer {director_token}'})

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Actor with the provided actor_id does not exist", response.data)

    def test_update_non_existing_movie(self):
        """Test PATCH /movies/<id> with non-existing movie."""
        updated_data = {
            "title": "Dial M for Murderousness",
            "release_year": 2022,
            "genre": "Comedy"
        }

        response = self.client.patch('/movies/9999', json=updated_data, headers={'Authorization': f'Bearer {director_token}'})

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Movie not found", response.data)

    def test_delete_non_existing_movie(self):
        """Test DELETE /movies/<id> with non-existing movie."""
        response = self.client.delete('/movies/9999', headers={'Authorization': f'Bearer {producer_token}'})

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Movie not found", response.data)

    def test_add_movie(self):
        """Test POST /movies route to add a new movie."""
        actor = Actor(name="Otm Shank", age=30)
        db.session.add(actor)
        db.session.commit()

        new_movie = {
            "title": "Inception",
            "release_year": 2010,
            "genre": "Sci-Fi",
            "actor_id": actor.id  # Use the actor created above
        }

        response = self.client.post('/movies', json=new_movie, headers={'Authorization': f'Bearer {director_token}'})
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        
        self.assertEqual(data['title'], "Inception")
        self.assertEqual(data['release_year'], 2010)
        self.assertEqual(data['genre'], "Sci-Fi")
        self.assertEqual(data['actor_id'], actor.id)

    def test_update_movie(self):
        """Test PATCH /movies/<id> route to update an existing movie."""
        actor = Actor(name="Otm Shank", age=30)
        db.session.add(actor)
        db.session.commit()

        movie = Movie(title="Dial M for Murderousness", release_year=2021, genre="Thriller", actor_id=actor.id)
        db.session.add(movie)
        db.session.commit()

        updated_data = {
            "title": "Dial M for Murderousness (Updated)",
            "release_year": 2012,
            "genre": "Mystery/Thriller",
        }

        response = self.client.patch(f'/movies/{movie.id}', json=updated_data, headers={'Authorization': f'Bearer {director_token}'})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(data['title'], "Dial M for Murderousness (Updated)")
        self.assertEqual(data['release_year'], 2012)
        self.assertEqual(data['genre'], "Mystery/Thriller")

    def test_delete_movie(self):
        """Test DELETE /movies/<id> route to delete a movie."""
        actor = Actor(name="Otm Shanks", age=30)
        db.session.add(actor)
        db.session.commit()

        movie = Movie(title="Dial M for Murderousness", release_year=2021, genre="Thriller", actor_id=actor.id)
        db.session.add(movie)
        db.session.commit()

        response = self.client.delete(f'/movies/{movie.id}', headers={'Authorization': f'Bearer {producer_token}'})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertTrue(data['success'])
        self.assertIn(f"Movie with ID {movie.id} has been deleted", data['message'])

if __name__ == '__main__':
    unittest.main()

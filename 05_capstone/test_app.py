  
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, Performance, db_drop_and_create_all
from config import tokens
from sqlalchemy import desc
from datetime import date


casting_assistant_auth_header = {
    'Authorization': tokens['casting-assistant']
}

casting_director_auth_header = {
    'Authorization': tokens['casting-director']
}

executive_producer_auth_header = {
    'Authorization': tokens['executive-producer']
}


class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['database_url']
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def test_create_new_actor(self):
        """Test POST new actor."""

        json_create_actor = {
            'name' : 'Crisso',
            'age' : 25
        } 

        res = self.client().post('/actors', json = json_create_actor, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)
    
    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name' : 'Crisso',
            'age' : 25
        } 

        res = self.client().post('/actors', json = json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
 
    def test_error_422_create_new_actor(self):
        """Test Error POST new actor."""

        json_create_actor_without_name = {
            'age' : 25
        } 

        res = self.client().post('/actors', json = json_create_actor_without_name, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors?page=1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        """Test GET all actors w/o Authorization."""
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_404_get_actors(self):
        """Test Error GET all actors."""
        res = self.client().get('/actors?page=1125125125', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def test_edit_actor(self):
        """Test PATCH existing actors"""
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/1', json = json_edit_actor_with_new_age, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    def test_error_400_edit_actor(self):
            res = self.client().patch('/actors/123412', headers = casting_director_auth_header)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            self.assertFalse(data['success'])

    def test_error_404_edit_actor(self):
        """Test PATCH with non valid id"""
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/123412', json = json_edit_actor_with_new_age, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_403_delete_actor(self):
        """Test DELETE existing actor with missing permissions"""
        res = self.client().delete('/actors/1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        """Test DELETE existing actor"""
        res = self.client().delete('/actors/1', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_actor(self):
        """Test DELETE non existing actor"""
        res = self.client().delete('/actors/15125', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def test_create_new_movie(self):
        """Test POST new movie."""

        json_create_movie = {
            'title' : 'Crisso Movie',
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_error_422_create_new_movie(self):
        """Test Error POST new movie."""

        json_create_movie_without_name = {
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie_without_name, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


    def test_get_all_movies(self):
        """Test GET all movies."""
        res = self.client().get('/movies?page=1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        """Test GET all movies w/o Authorization."""
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_404_get_movies(self):
        """Test Error GET all movies."""
        res = self.client().get('/movies?page=1125125125', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def test_edit_movie(self):
        """Test PATCH existing movies"""
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_error_400_edit_movie(self):
        """Test PATCH with non valid id json body"""
        res = self.client().patch('/movies/1', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/123412', json = json_edit_movie, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def test_error_401_delete_movie(self):
        """Test DELETE existing movie w/o Authorization"""
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_error_403_delete_movie(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        """Test DELETE existing movie"""
        res = self.client().delete('/movies/1', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/151251', headers = executive_producer_auth_header) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()
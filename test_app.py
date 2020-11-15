import os
import unittest
import json
from app import create_app
from models import setup_db, drop_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        print("setup")
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = 'postgres://marshall@localhost:5432/{}'.format(self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Jonah Hill',
            'age': 37,
            'gender': 'male'
        }

        self.actor_update = {
            'age': 38
        }

        self.new_movie = {
            'title': 'Superbad',
            'release_date': '8/17/2007'
        }

        self.movie_update = {
            'release_date': '9/20/2008'
        }

        self.executive_producer = {'Authorization': 'Bearer {}'.format(os.environ['EXECUTIVE_JWT'])}
        self.executive_producer_no_bearer = {'Authorization': '{}'.format(os.environ['EXECUTIVE_JWT'])}
        self.casting_director = {'Authorization': 'Bearer {}'.format(os.environ['CASTING_DIRECTOR_JWT'])}
        self.casting_assistant = {'Authorization': 'Bearer {}'.format(os.environ['ASSISTANT_JWT'])}

    def test001_create_new_actor_by_casting_director(self):
        print("1")
        res = self.client().post('/actor', headers=self.casting_director, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test002_405_create_new_actor(self):
        print("2")
        res = self.client().patch('/actor', headers=self.executive_producer, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test003_get_actors_by_casting_assistant(self):
        print("3")
        res = self.client().get('/actors', headers=self.casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']), 1)

    def test004_404_get_actors(self):
        print("4")
        res = self.client().get('/actor', headers=self.executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test005_create_new_movie(self):
        print("5")
        res = self.client().post('/movie', headers=self.executive_producer, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test006_405_create_new_movie(self):
        print("6")
        res = self.client().patch('/actor', headers=self.executive_producer, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test007_get_movies(self):
        print("7")
        self.client().post('/movie', headers=self.executive_producer, json=self.new_movie)
        res = self.client().get('/movies', headers=self.executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test008_405_get_movies(self):
        print("8")
        self.client().post('/movie', headers=self.executive_producer, json=self.new_movie)
        res = self.client().get('/movie', headers=self.executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test009_update_actor(self):
        print("9")
        res = self.client().patch('/actor/1', headers=self.executive_producer, json=self.actor_update)
        data = json.loads(res.data)
        actor = Actor.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['age'], 38)

    def test010_400_update_actor(self):
        print("10")
        self.client().post('/actor', headers=self.executive_producer, json=self.new_actor)
        res = self.client().patch('/actor/300', headers=self.executive_producer, json={"age": 36})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test011_update_movie(self):
        print("11")
        res = self.client().patch('/movie/1', headers=self.executive_producer, json=self.movie_update)
        data = json.loads(res.data)
        movie = Movie.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['title'], 'Superbad')

    def test012_400_update_movie(self):
        print("12")
        self.client().patch('/movie', headers=self.executive_producer, json=self.new_movie)
        res = self.client().patch('/movie/300', headers=self.executive_producer, json={"title": "superman"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test013_delete_actor(self):
        print('13')
        res = self.client().delete('/actor/1', headers=self.executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test014_delete_movie(self):
        print('14')
        res = self.client().delete('/movie/1', headers=self.executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test015_create_new_actor_by_casting_assistant(self):
        print("15")
        res = self.client().post('/actor', headers=self.casting_assistant, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['description'], "Permission not found.")

    def test016_delete_movie_by_casting_director(self):
        print("16")
        self.client().post('/movie', headers=self.executive_producer, json=self.new_movie)
        res = self.client().delete('/movie/1', headers=self.casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['description'], "Permission not found.")

    def test017_delete_movie_by_executive_producer_no_bearer(self):
        print("17")
        self.client().post('/movie', headers=self.executive_producer, json=self.new_movie)
        res = self.client().delete('/movie/1', headers=self.executive_producer_no_bearer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Authorization header must start with "Bearer".')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

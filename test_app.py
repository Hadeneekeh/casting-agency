import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56QkNRVEkwUkVWQ016STNOVUV5UmtSQk1EQXpSVFl6UkRVM05qRXlRemc0TmpWRFFqRXpSZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYXV0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1YTEzNzg5OWQwODkwZDUzMGYxOGVjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzI3MjQ5MiwiZXhwIjoxNTgzMzU4ODkyLCJhenAiOiJaeGNKaXZRcVg4N3VZMUQ5eWZHaGE2OHpkSjJ0TjBPZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJlZGl0OmFjdG9yIiwiZWRpdDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.IFKwJ_6doJq9WjD4FW_iY-xpqCHYOWoGWT7t9AQDs8xGKfv8GYzOSPWEynnvVkJ1Dt89HwhvkK9tR4ODIudwqNX_gawMZEC9CP4Sm-Bt40wKS_wH8H6phTvNAdL7vE8ek1O-bAGAfqrgrm7suv8965HEAoLykdeVuqR2gHXzgjl6YT2zgUTUaR_03T_BGHYs00pnWI6-qp2AqrlY2Gxf1tDdQuZLuabKdCQYmJejZBkmCORgKFXx7S7pW_7pguIhL0JRhgG8A-VXLDSuuAw5gHCHabKag9S7YsqG2ihkXzpkg2AGgbBMB5uUn7j4lRs4AxR2cKw7DUiTvgvObh3icQ'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56QkNRVEkwUkVWQ016STNOVUV5UmtSQk1EQXpSVFl6UkRVM05qRXlRemc0TmpWRFFqRXpSZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYXV0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1YTEzYzA5OWQwODkwZDUzMGYxOTIxIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzI3MjcwMCwiZXhwIjoxNTgzMzU5MTAwLCJhenAiOiJaeGNKaXZRcVg4N3VZMUQ5eWZHaGE2OHpkSjJ0TjBPZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.E2qVi7mEGVa8UF6CGPJ2xIYpV8MUEZ0VEK6KZUbLorO_CGIRvhxmfDl6M2JPLmSfunBRzH9G1xNwZNji8Rt4HmH5URO63KrJRDG5QMzqmtURSkMl_gyGNSoXR3Ifib60Lf4OAwn9611pZPEFCGeJtbKqPMVLBbxkfQ3QOAFNT1URikAq58aAn3UOJZRAG23_bdArTClP9EBS5M6Ey5t1I_lOAHXrWCxTQu8BxjrbaWpl1zPIRv3yWcnwDxaLvE8J4ICBBDZBIr3LlFCyGBDVpDYN96iYZwUKdppXztQ4qRY3liZSzCIPrnw9Qf3JlQbfZK3maH27DpJHVCB2_fKCGA'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56QkNRVEkwUkVWQ016STNOVUV5UmtSQk1EQXpSVFl6UkRVM05qRXlRemc0TmpWRFFqRXpSZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYXV0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1YTE0NTEyN2ZjMzIwZDNiY2VjMzE2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzI3MjkxNiwiZXhwIjoxNTgzMzU5MzE2LCJhenAiOiJaeGNKaXZRcVg4N3VZMUQ5eWZHaGE2OHpkSjJ0TjBPZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvciIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.oWpS5pPh6NKui3MnlMPHxrT6EK0pexs6FzUrb_YYgPGt_pWX-pIHFIMvzTMJhpH9S1l-pfVFvJcxUdrFDcEl3E061xUS4JIFrYpMutay71Q7HXOvZF3CohnxQziua_hYX0JarKJ5bqba32TcoakStxx1JMDOY-hFwUzng_qhhP352wqbzqBbVl-uEbqphJ7nOz-aSUenPawj_xCkumb7wdUaGCYKBWmv9jHmD2Rt5hdFO03SMhp-l5Mgu6nnfU2mGJdVF3RFTCbRMTWV5Q3L4QoFWXvGIVA3zxE1Cq0O1AqpCuFZN_3SpBrMH2mo93R5I9xY9bKdJDzpQgMwxSSyvg'

class TriviaTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DATABASE_URL')
        setup_db(self.app)


    def tearDown(self):
        """Executed after reach test"""
        pass


    #ACTORS
    def test_add_actors(self):
        response= self.client().post(
            '/actors',
            json={'name': 'Kafilat', 'age': '23', 'gender': 'female'},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['actor'])


    def test_bad_request_in_add_actor(self):
        response= self.client().post(
            '/actors',
            json={'name': '', 'age': '', 'gender': ''},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'Bad Request, please check your inputs')
        self.assertEqual(data['success'], False)


    def test_edit_actors(self):
        response= self.client().patch(
            '/actors/2',
            json={'name': 'Kafee'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['actor'])


    def test_not_found_in_edit_actor(self):
        response= self.client().patch(
            '/actors/1000',
            json={'name': 'K'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)


    def test_bad_request_in_edit_actor(self):
        response= self.client().patch(
            '/actors/2',
            json={'name': ''},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'Bad Request, please check your inputs')
        self.assertEqual(data['success'], False)


    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delete'], '1')
        self.assertTrue(data['success'])


    def test_not_found_delete_actor(self):
        response = self.client().delete(
            '/actors/1005',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    #MOVIES
    def test_add_movies(self):
        response= self.client().post(
            '/movies',
            json={'title': 'Awesomeness', 'release_date': '2020/02/01'},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['movie'])


    def test_bad_request_in_add_movie(self):
        response= self.client().post(
            '/movies',
            json={'title': '', 'release_date': ''},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'Bad Request, please check your inputs')
        self.assertEqual(data['success'], False)


    def test_edit_movie(self):
        response= self.client().patch(
            '/movies/2',
            json={'title': 'Jumanji'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['movie'])


    def test_not_found_in_edit_movie(self):
        response= self.client().patch(
            '/movies/1000',
            json={'title': 'J'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)


    def test_bad_request_in_edit_movie(self):
        response= self.client().patch(
            '/movies/2',
            json={'title': ''},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'Bad Request, please check your inputs')
        self.assertEqual(data['success'], False)


    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['delete'], '1')
        self.assertTrue(data['success'])

    def test_not_found_delete_movie(self):
        response = self.client().delete(
            '/movies/1005',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
            )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    #UNAUTHORISED TEST CASES
    def test_unauthorised_add_movies(self):
        response= self.client().post(
            '/movies',
            json={'title': 'Awesomeness', 'release_date': '2020/02/01'},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])


    def test_unauthorised_add_actors(self):
        response= self.client().post(
            '/actors',
            json={'name': 'Kafilat', 'age': '23', 'gender': 'female'},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])


    def test_unauthorised_in_edit_actor(self):
        response= self.client().patch(
            '/actors/1',
            json={'name': 'K'},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])


    def test_unauthorised_delete_movie(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
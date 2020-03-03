import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56QkNRVEkwUkVWQ016STNOVUV5UmtSQk1EQXpSVFl6UkRVM05qRXlRemc0TmpWRFFqRXpSZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYXV0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1YTEzNzg5OWQwODkwZDUzMGYxOGVjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzIyNzAwOSwiZXhwIjoxNTgzMzEzNDA5LCJhenAiOiJaeGNKaXZRcVg4N3VZMUQ5eWZHaGE2OHpkSjJ0TjBPZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJlZGl0OmFjdG9yIiwiZWRpdDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.qx0LdA7mIYlFmDiOQpLQJRDv63bY0upOra2kB3zmbvlszcCB4feFffvl5ZT-rMdIGqGfUW61_Jero2QZKgtIUGBsBOO9s97hkrE2liFcVYy3nNiiF5AT3SBwxJRTYnWkrXCrad6BY1Ia7MGZIHljIPGzZiAUby8eXPQpfRyQxdNEg14GpJQWA29tnTvhyOWYjxE0MyE7hFSSGpGP1FZYk7Qn4deyFBnMMZ4IjEpiwM3cX6puW_S5cZwYzDeiZXRGkspdA8_FjSElDduftAg6acN2rupaA7bX2dZyV9TqXU8gWURfFk7wJTuvgtDZWVr8HIxyiVQGuvlOOKcrcIr3aw'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56QkNRVEkwUkVWQ016STNOVUV5UmtSQk1EQXpSVFl6UkRVM05qRXlRemc0TmpWRFFqRXpSZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYXV0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1YTEzYzA5OWQwODkwZDUzMGYxOTIxIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzIyNzIxNCwiZXhwIjoxNTgzMzEzNjE0LCJhenAiOiJaeGNKaXZRcVg4N3VZMUQ5eWZHaGE2OHpkSjJ0TjBPZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.UCt9CZJjyTq9GzV_QKSD2Nu71fwU3Q2-a_YYYZznctYDKp_12VVCcSQhdxUDFtw65PhfZNIS-Ttb0JT0_p_i9e8-CbsfbVKWqykSgma0FKapTXctnPp_8iO4Hy6g6uy5AEwga5M32seonXa6J_tOzEOPYEHwHnrUww26l0Sk9bu3eKlZVmkwSSpeJOSJZcmzhopMmSLfVDxhm49fIYCgkpxA9S9odNeRCuhcaCK4O4t_HW9ZDtNe06yJPaf9l1-TL077v6cWq7ZIjoKRCf3lG8pSwb87YgCjA2chVmt-StW7u1xnyzwgJ1vyTWmoH0LkqhDITO9Nuzv7k1wRqKrUmg'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56QkNRVEkwUkVWQ016STNOVUV5UmtSQk1EQXpSVFl6UkRVM05qRXlRemc0TmpWRFFqRXpSZyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYXV0aC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU1YTE0NTEyN2ZjMzIwZDNiY2VjMzE2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzIyNzEwMywiZXhwIjoxNTgzMzEzNTAzLCJhenAiOiJaeGNKaXZRcVg4N3VZMUQ5eWZHaGE2OHpkSjJ0TjBPZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvciIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.D0yvLw2TkY-MekA2YkhwBaXx4ERi7Y95q9V8c0ib3AJzdGsqGSHgiwcY4efwelI0ajMzctZT9OF7HbfFqCCr6yHwqBo7UXb65eIftYa5NHo0UM3YD_Bs8eJY6M1hmJUnDyuM1Tgts5XuypFsxyN96TAeJj-GRRi14ZhPCyf3NTEaVQ8YpvOv4GV-PhzXdFh3Gz3XAst-Cgh1nmImhn6xiuS-poF4hHQrUcFzTsI1By0ujKo-ze7yB6qKGR7Y6ozwHaOK-nYSLEqijl_pc7dcdL02VrtPC2F-_oeXBvNfvWF1VB6v9QRpi8qiWVtFZIEjDBuw0lraVawa4ahjCya2Bg'

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
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Home route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to the casting agency'
        })

    # Actor routes
    @app.route('/actors')
    @requires_auth('get:actors')
    def list_actors(jwt):
        try:
            actors = Actors.query.all()
            formatted_actors = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': formatted_actors
            }), 200
        except Exception as e:
            abort(500)

    @app.route('/actors', methods=['POST'])
    @requires_auth("add:actors")
    def add_actor(jwt):
        get_input = request.get_json()

        name = get_input["name"]
        age = get_input["age"]
        gender = get_input["gender"]
        new_actor = Actors(name=name, gender=gender, age=age)
        if new_actor.name == '' or new_actor.age == '' or new_actor.gender == '':
            abort(400)
        try:
            new_actor.insert()
            return jsonify({
                "success": True,
                "actor": new_actor.format()}), 201
        except Exception as e:
            abort(422)

    @app.route("/actors/<id>", methods=["PATCH"])
    @requires_auth("edit:actor")
    def update_actor(jwt, id):
        name = request.get_json()["name"]
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)
        if name == "":
            abort(400)
        try:
            actor.name = name
            actor.update()

            return jsonify({
                "success": True,
                "actor": [actor.format()]
            }), 200
        except Exception as e:
            abort(422)

    @app.route("/actors/<id>", methods=["DELETE"])
    @requires_auth("delete:actor")
    def delete_actor(jwt, id):
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)
        try:
            actor.delete()

            return jsonify({
                "success": True,
                "delete": id
            }), 200
        except Exception as e:
            abort(500)

    # Movie routes
    @app.route('/movies')
    @requires_auth('get:movies')
    def list_movies(jwt):
        try:
            movies = Movies.query.all()
            formatted_movies = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': formatted_movies
            }), 200
        except Exception as e:
            abort(500)

    @app.route('/movies', methods=['POST'])
    @requires_auth("add:movies")
    def add_movie(jwt):
        get_input = request.get_json()

        title = get_input["title"]
        release_date = get_input["release_date"]

        new_movie = Movies(title=title, release_date=release_date)
        if new_movie.title == '' or new_movie.release_date == '':
            abort(400)
        try:
            new_movie.insert()

            return jsonify({
                "success": True,
                "movie": new_movie.format()
            }), 201
        except Exception as e:
            print(e)
            abort(422)

    @app.route("/movies/<id>", methods=["PATCH"])
    @requires_auth("edit:movies")
    def update_movie(jwt, id):
        title = request.get_json()["title"]
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)
        movie.title = title
        if movie.title == "":
            abort(400)
        try:
            movie.update()

            return jsonify({
                "success": True,
                "movie": [movie.format()]
            }), 200
        except Exception as e:
            print(e)
            abort(422)

    @app.route("/movies/<id>", methods=["DELETE"])
    @requires_auth("delete:movie")
    def delete_movie(jwt, id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)
        try:
            movie.delete()

            return jsonify({
                "success": True,
                "delete": id
            }), 200
        except Exception as e:
            abort(500)

    # Error Handling
    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({
                "success": False,
                "error": 500,
                "message": "Server Error",
                }),
            500,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 400,
                    "message": "Bad Request, please check your inputs",
                }
            ),
            400,
        )

    @app.errorhandler(401)
    def unathorized(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 401,
                    "message": error.description,
                }
            ),
            401
        )

    @app.errorhandler(403)
    def forbidden(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 403,
                    "message": "You are not allowed to access this resource",
                }
            ),
            403,
        )

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

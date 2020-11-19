from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import *
from auth import AuthError, requires_auth


# --------App Initialization----------------

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

# -------Endpoints----------------------

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        try:
            actors = Actor.query.all()
            return jsonify({
                "success": True,
                "actors": [actor.format() for actor in actors]
            })
        except():
            abort(404)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        try:
            movies = Movie.query.all()
            return jsonify({
                "success": True,
                "movies": [movie.format() for movie in movies]
            })
        except():
            abort(404)

    @app.route('/actor/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, id):
        try:
            actor = Actor.query.get(id)

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                "success": True,
                "deleted": actor.id
            })

        except():
            abort(422)

    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                "success": True,
                "deleted": movie_id
            })

        except():
            abort(422)

    @app.route('/actor', methods=["POST"])
    @requires_auth('post:actor')
    def create_actor(token):
        try:
            body = request.get_json()

            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()

            return jsonify({
                'success': True,
                'created': Actor.format(new_actor)
            })
        except():
            abort(422)

    @app.route('/movie', methods=["POST"])
    @requires_auth('post:movie')
    def create_movie(token):
        try:
            body = request.get_json()

            title = body.get('title')
            release_date = body.get('release_date')

            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()

            return jsonify({
                'success': True,
                'created': Movie.format(new_movie)
            })
        except():
            abort(422)

    @app.route('/actor/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(token, id):
        try:
            body = request.get_json()
            actor = Actor.query.get(id)
            if actor is None:
                abort(404)
            if 'name' in body:
                actor.name = body['name']
            elif 'age' in body:
                actor.age = body['age']
            elif 'gender' in body:
                actor.gender = body['gender']
            else:
                abort(400)

            actor.update()

            return jsonify({
                'success': True,
                'updated': actor.format()
            })
        except():
            abort(400)

    @app.route('/movie/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(token, id):
        try:
            body = request.get_json()
            movie = Movie.query.get(id)
            if movie is None:
                abort(404)
            if 'title' in body:
                movie.title = body['title']
            elif 'release_date' in body:
                movie.release_date = body['release_date']
            else:
                abort(400)

            movie.update()

            return jsonify({
                'success': True,
                'updated': movie.format()
            })

        except():
            abort(400)

    @app.route('/casting', methods=['POST'])
    @requires_auth('post:cast')
    def create_cast(token):
        try:
            body = request.get_json()

            movie_id = body['movie_id']
            actor_id = body['actor_id']

            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(404)

            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404)

            movie.cast.append(actor)
            movie.update()

            return jsonify({
                'success': True,
                'cast member added': f" {actor.name} added to the {movie.title} cast."
            })
        except():
            abort(400)

# -------Error Handling--------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

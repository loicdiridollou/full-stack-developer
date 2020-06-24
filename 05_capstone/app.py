import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
#from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance
from config import pagination

ROWS_PER_PAGE = pagination['example']

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)


    def paginate_results(request, selection):
        '''Paginates and formats database queries
        Parameters:
        * <HTTP object> request, that may contain a "page" value
        * <database selection> selection of objects, queried from database
        
        Returns:
        * <list> list of dictionaries of objects, max. 10 objects
        '''
        # Get page from request. If not given, default to 1
        page = request.args.get('page', 1, type=int)
        
        # Calculate start and end slicing
        start =  (page - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        # Format selection into list of dicts and return sliced
        objects_formatted = [object_name.format() for object_name in selection]
        return objects_formatted[start:end]



    @app.route('/')
    def index_page():
        return jsonify({"message": "Hello World!"})


    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def get_actors(payload):
        pass


    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def insert_actors(payload):
        pass


    @app.route('/actors/<actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actors(payload, actor_id):
        pass


    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        pass


    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movies(payload):
        pass


    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def insert_movies(payload):
        pass


    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movies(payload, movie_id):
        pass


    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        pass


    #----------------------------------------------------------------------------#
    # Error Handlers
    #----------------------------------------------------------------------------#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404


    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({"success": False, "error": AuthError.status_code, "message": AuthError.error}), 401


    return app



app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

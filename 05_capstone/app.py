import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
#from models import db_drop_and_create_all, setup_db, Actor, Movie, Performance
from config import pagination


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

APP = create_app()

@APP.route('/')
def index_page():
    return jsonify({"message": "Hello World!"})



if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

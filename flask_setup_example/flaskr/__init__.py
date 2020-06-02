from flask import Flask, jsonify
import os

def create_app(test_config = None):
    app = Flask(__name__)

    app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'))
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass   

    @app.route('/')
    def hello_world():
        return jsonify({'message':'Hello, World!'})
    
    return app
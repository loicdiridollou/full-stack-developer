import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()


def get_all_drinks(recipe_format):
    all_drinks = Drink.query.order_by(Drink.id).all()

    if recipe_format.lower() == 'short':
        drinks_formatted = [drink.short() for drink in all_drinks]
    elif recipe_format.lower() == 'long':
        drinks_formatted = [drink.long() for drink in all_drinks]
    else:
        abort(500)
    return drinks_formatted



## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods = ["GET"])
def get_drinks():
    return jsonify({"success": True, "drinks": get_all_drinks('short')})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail', methods = ["GET"])
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    return jsonify({"success": True, 'drinks': get_all_drinks("long")})

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks',  methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    """Creates new drink and returns it to client"""
    
    body = request.get_json()

    if body is None:
        return 

    new_drink = Drink(title = body['title'], recipe = """{}""".format(body['recipe']))
    
    new_drink.insert()
    new_drink.recipe = body['recipe']
    return jsonify({
    'success': True,
    'drinks': Drink.long(new_drink)
    })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<drink_id>', methods = ["PATCH"])
@requires_auth('patch:drinks')
def patch_drinks(drink_id):
    body = request.get_json()
    
    if not body:
        abort(400)
    
    up_title = body.get('title', None)
    up_recipe = body.get('recipe', None)

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    
    if up_title:
        drink.title = body['title']
    if up_recipe:
        drink.recipe = body['recipe']
    
    drink.update()
    
    return jsonify({
    'success': True,
    'drinks': [Drink.long(drink)]
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<drink_id>', methods = ["DELETE"])
@requires_auth('delete:drinks')
def delete_drinks(drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    
    if not drink:
        abort(401)

    
    drink.delete()
    
    return jsonify({
    'success': True,
    'delete': 'drink_id'
    })


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODODONE implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404



'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authentification_failed(AuthError):
    return jsonify({"success": False, "error": AuthError.status_code, "message": AuthError.error}), 401

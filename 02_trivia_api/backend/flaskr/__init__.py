import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import time

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
        
    '''
    @TODODONE: Set up CORS. Allow '*' for origins. Delete the sample route 
    after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]

        return questions[start:end]



    @app.route('/')
    def hello_world():
        return 'Hello World!'


    '''
    @TODODONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 
            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODODONE: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories', methods = ['GET'])
    def get_categories():
        categories = Category.query.all()

        if not categories:
            abort(404)
        
        categories_all = [cat.format() for cat in categories]

        categories_returned = []
        for cat in categories_all:
            categories_returned.append(cat['type'])
        
        return jsonify({"success": True, "categories": categories_returned})

    

    '''
    @TODODONE: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 


    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for 
    three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        questions_paginated = paginate_questions(request, selection)
        if len(questions_paginated) == 0:
            abort(404)
        
        
        
        categories = Category.query.all()
        categories_all = [category.format() for category in categories]
        
        # Initialize empty list to be filled & returned
        categories_returned = []
        for cat in categories_all:
            categories_returned.append(cat['type'])
        return jsonify({
        'success': True,
        'questions': questions_paginated,
        'total_questions': len(selection),
        'categories' : categories_returned,
        'current_category' : categories_returned
        })



    '''
    @TODODONE: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will 
    be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<question_id>', methods = ['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404, {'Question does not exist'})
        try:
            question.delete()
            return jsonify({"success": True, "deleted": question_id})
        except:
            abort(422)

    '''
    @TODODONE: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    '''
    @TODODONE: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions', methods = ['POST'])
    def create_question():
        body = request.get_json()
        if not body:
            abort(400)
        search_term = body.get('search_term', None)
        
        if search_term == '':
            abort(404)
            
        if search_term:
            questions = Question.query.filter(Question.question.contains(search_term)).all()

            if not questions:
                abort(404, {'message': 'no questions that contains "{}" found.'.format(search_term)})
            
            questions_found = [question.format() for question in questions]
            selections = Question.query.order_by(Question.id).all()
            
            categories = Category.query.all()
            categories_all = [category.format() for category in categories]

            return jsonify({
                'success': True,
                'questions': questions_found,
                'total_questions': len(selections),
                'current_category' : categories_all
            })
        
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        if not new_answer or not new_question:
            abort(400)
        if not new_difficulty or not new_category:
            abort(400)
        
        try:
            question = Question(question = new_question, difficulty = new_difficulty, 
                answer = new_answer, category = new_category)
            question.insert()
            selections = Question.query.order_by(Question.id).all()
            questions_paginated = paginate_questions(request, selections)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': questions_paginated,
                'total_questions': len(selections)
            })

        except:
            abort(422)




    '''
    @TODODONE: 
    Create a GET endpoint to get questions based on category. 

    TODO TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<category_id>/questions', methods = ['GET'])
    def get_questions_by_cat(category_id):
        print(str(int(category_id)+1))
        selection = Question.query.filter(Question.category == str(int(category_id)+1)).order_by(Question.id).all()
        print([ques for ques in selection])
        questions_paginated = paginate_questions(request, selection)
        if len(questions_paginated) == 0:
            abort(400)
        
        
        
        categories = Category.query.all()
        categories_all = [category.format() for category in categories]
        
        # Initialize empty list to be filled & returned
        categories_returned = []
        for cat in categories_all:
            categories_returned.append(cat['type'])
        return jsonify({
        'success': True,
        'questions': questions_paginated,
        'total_questions': len(selection),
        'categories' : categories_returned,
        'current_category' : category_id
        })


    '''
    @TODODONE: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods = ['POST'])
    def play():

        body = request.get_json()

        if not body:
            abort(400)
        
        previous_questions = body.get('previous_questions', None)
        current_category = body.get('current_category', None)
        if current_category:
            cat = Category.query.filter(Category.id = str(current_category['id'])).one_or_none()
            if cat is None:
                abort(404)

        if previous_questions:
            if current_category:
                if current_category == "0":
                    questions_raw = Question.query.all()
                else:
                    questions_raw = Question.query.filter(Question.category == 
                        str(current_category['id'])).filter(Question.id.notin_(previous_questions)).all()
            else:
                questions_raw = Question.query.filter(Question.id.notin_(previous_questions)).all()
                if len(questions_raw) == 0:
                    return jsonify({"success": True, "question": None})

        else:
            if current_category:
                if current_category == "0":
                    questions_raw = Question.query.all()
                else:
                    questions_raw = Question.query.filter(Question.category == str(current_category['id'])).all()
            else:
                questions_raw = Question.query.all()
        
        questions = [question.format() for question in questions_raw]
        random_question = questions[random.randint(0, len(questions))]

        return jsonify({"success": True, "question": random_question})



    '''
    @TODODONE: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404
    
    @app.errorhandler(405)
    def ressource_not_found(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, 
            "error": 422, 
            "message": "Unprocessable"}), 422

    return app

      
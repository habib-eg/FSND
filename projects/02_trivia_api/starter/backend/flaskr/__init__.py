import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from starter.backend.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def categories():

        categories = Category.query.all()

        return jsonify({
            "success": True,
            "categories": {category.id: category.type for category in categories},
            "total_categories": len(categories),
        })

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions')
    def questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()

        formatted_questions = [question.format() for question in questions][start:end]

        # if not len(formatted_questions) and page != 1:
        #     abort(404)
        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "categories": {category.id: category.type for category in Category.query.all()},
            "current_category": None
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        Question.query.filter_by(id=question_id).first_or_404().delete()
        return jsonify({
            "success": True,
            "message": "Question deleted successfully."
        })

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        form = request.get_json()
        try:
            question = Question(question=form['question'], answer=form['answer'], difficulty=form['difficulty'],
                                category_id=form['category']).insert()
            return jsonify({
                "success": True,
                "message": "Question created successfully."
            })
        except:
            db.session.rollback()
        finally:
            db.session.close()

        abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        search = request.get_json()['searchTerm']
        questions = Question.query.filter(Question.question.ilike("%{}%".format(search))).all()
        formatted_questions = [question.format() for question in questions][start:end]

        # if not len(formatted_questions) and page != 1:
        #     abort(404)

        return jsonify({
            "success": True,
            "questions": formatted_questions[start:end],
            "total_questions": len(formatted_questions),
            "categories": {category.id: category.type for category in Category.query.all()},
            "current_category": None
        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category = Category.query.get_or_404(category_id)
        questions = category.questions

        return jsonify({
            "success": True,
            "questions": [question.format() for question in questions],
            "totalQuestions": len(questions),
            "currentCategory": category.format(),
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        jsonData = request.get_json()
        previous_questions = jsonData['previous_questions']
        quiz_category = jsonData['quiz_category']
        print(jsonData)
        print(previous_questions)

        question = Question.query.filter(Question.id.notin_(previous_questions),
                                         Question.category_id == quiz_category['id']).first()
        if question is not None:
            question = question.format()

        return jsonify({
            "question": question
        })

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'message': 'Not Found',
            'code': 404,
            'success': False,
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'message': 'resource Not Found',
            'code': 422,
            'success': False,
        }), 422

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            'message': 'Bad Request',
            'code': 400,
            'success': False,
        }), 400

    return app

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# paginate questions
def paginate_questions(request, select_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in select_questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # after request decorator to set Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # get all categories

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        format_categories = {category.id: category.type for category in
                             categories}

        return jsonify({
            'success': True,
            'categories': format_categories,
            'total_categories': len(format_categories)
          })

    # get all questions

    @app.route('/questions')
    def get_questions():
        select_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, select_questions)
        categories = Category.query.all()
        format_categories = {category.id: category.type for category
                             in categories}
        current_category = Category.query.filter_by(id=current_questions[0]
                                                    ['category']).first()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(select_questions),
            'categories': format_categories,
            'current_category': current_category.type
          })

    # delete a question

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(422)

            question.delete()
            select_questions = Question.query.order_by(Question.id).all()

            return jsonify({
                'success': True,
                'question_deleted': question.id,
                'total_questions': len(select_questions),
              })

        except Exception:
            abort(422)

    # create a new question

    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()
        new_question = body.get('question', None)
        question_answer = body.get('answer', None)
        question_category = body.get('category', None)
        question_difficulty = body.get('difficulty', None)

        if new_question is None:
            abort(422)

        try:
            question = Question(question=new_question, answer=question_answer,
                                category=question_category,
                                difficulty=question_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'question_created': question.id,
                'total_questions': len(Question.query.all())
              })

        except Exception:
            abort(422)

    # search questions

    @app.route('/questions/search', methods=['POST'])
    def get_questions_by_search_term():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        select_questions = Question.query.filter(Question.question.ilike
                                                 (f'%{search_term}%')).all()
        current_questions = paginate_questions(request, select_questions)
        current_category = Category.query.filter_by(id=current_questions[0]
                                                    ['category']).first()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(select_questions),
            'current_category': current_category.type
          })

    # get questions by category

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        select_questions = Question.query.filter_by(category=category_id).all()
        current_questions = paginate_questions(request, select_questions)
        category = Category.query.filter_by(id=category_id).one_or_none()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(select_questions),
            'current_category': category.type,
          })

    # play quiz

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        category_id = quiz_category['id']

        # getting questions from a specific category or all categories
        if category_id:
            questions = Question.query.filter_by(category=category_id).all()
        else:
            questions = Question.query.all()

        format_questions = [question.format() for question in questions]
        # generating a random question
        random_question = random.choice(format_questions)

        # checking if id random question is in previous questions
        while random_question['id'] in previous_questions:
            random_question = random.choice(format_questions)
            if len(previous_questions) == len(format_questions):
                return jsonify({
                    'question': None
                  })
                break
        else:
            return jsonify({
                'success': True,
                'question': random_question,
                'question_id': random_question['id']
              })

    # 404 error handler

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
          }), 404

    # 422 error handler

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
          }), 422

    # 405 error handler

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
          }), 405

    # 400 error handler

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
          }), 400

    # 500 error handler

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
          }), 500

    return app

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "abc", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Who was the first president of Kenya?",
            "answer": "Jomo Kenyatta",
            "category": 4,
            "difficulty": 1
        }

        self.search_term = {
            "searchTerm": "who"
        }

        self.quiz = {
            "previous_questions": [],
            "quiz_category": {"id": 1, "type": "Science"}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test for getting categories

    def test_get_categories(self):
        resp = self.client().get('/categories')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_404_requesting_invalid_category(self):
        resp = self.client().get('/categories/4')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test for getting all questions

    def test_get_questions(self):
        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    def test_404_requesting_invalid_page(self):
        resp = self.client().get('/questions?page=100')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test for getting questions by category

    def test_get_questions_by_category(self):
        resp = self.client().get('/categories/4/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 'History')
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_404_requesting_invalid_page(self):
        resp = self.client().get('/categories/4/questions?page=100')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test for creating a new question

    def test_create_new_question(self):
        resp = self.client().post('/questions', json=self.new_question)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_created'])
        self.assertTrue(data['total_questions'])

    def test_405_failed_to_create_question(self):
        resp = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Test for deleting a question

    def test_delete_question(self):
        resp = self.client().delete('/questions/14')
        data = json.loads(resp.data)

        question = Question.query.filter_by(id=14).one_or_none()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_deleted'], 14)
        self.assertTrue(data['total_questions'])

    def test_422_question_doesnt_exist(self):
        resp = self.client().delete('/questions/100')
        data = json.loads(resp.data)

        question = Question.query.filter_by(id=100).one_or_none()

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test for search

    def test_get_questions_by_search_term(self):
        resp = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions']))

    def test_404_invalid_search_term(self):
        resp = self.client().post('/questions/search/100',
                                  json=self.search_term)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  Test for play quiz

    def test_get_quiz_questions(self):
        resp = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_cannot_load_questions(self):
        resp = self.client().post('/quizzes/100', json=self.quiz)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

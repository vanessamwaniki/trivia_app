# API Documentation
## Introduction
The trivia_app API is an application that allows a player to play a trivia quiz game with questions that are randomly generated.

It accepts and returns JSON objects.

## Getting Started
Base Url:
The trivia app currently runs locally and is hosted on default localhost `http://127.0.0.1:5000/`

API Keys:
The trivia app currently does not use API Keys or any authentication method

## Error Handling
Trivia API handles the following errors if a request fails:
- 404: resource not found
- 422: unprocessable
- 400: bad request
- 500: internal server error

The errors are returned as JSON objects.
Example of a returned 404 error:
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```
## Pagination
The Trivia API handles pagination for questions. It returns 10 questions per page.

You can include a request argument to choose the page number.

Try `curl http://127.0.0.1:5000/questions?page=2`

## API End Points
### GET Categories `/categories`
End point to get a list of all categories.

Returns all categories as a dictionary with category id as key and string type as value, total number of categories and a success value.

Takes no request arguments.

Try `curl http://127.0.0.1:5000/categories`

Reponse:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "totalCategories": 6
}
```

### GET Questions `/questions?page=${integer}`
End point to get all questions in a given page.

Takes a page request argument to get a specific page. `?page=${integer}`

Returns questions (10 questions for a page), total number of questions, all categories as a dictionary, the current category, and a success value

Try `curl http://127.0.0.1:5000/questions?page=1`

Response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": "Entertainment",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "totalQuestions": 21
}
```

### GET questions `/categories/${category_id}/questions` -by category
Endpoint to get questions by category using the category id.

Takes in the id (integer) of the category as an argument.

Returns an object with all questions in the specific category, total questions in that category, the string type of the current category, and a success value.

Try `http://127.0.0.1:5000/categories/4/questions` 

Response:
```
{
    "currentCategory": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Jomo Kenyatta",
            "category": 4,
            "difficulty": 1,
            "id": 27,
            "question": "Who was the first president of Kenya?"
        }
    ],
    "success": true,
    "totalQuestions": 4
}
```

### DELETE question `/questions/${question_id}`
Endpoint to delete a question using the id of the question.

Takes the question id (integer) as an argument.

Returns the id of the deleted question, total number of questions, and a success value.

Try `curl http://127.0.0.1:5000/questions/25`

Response:
```
{
    "question_deleted": 27,
    "success": true,
    "totalQuestions": 18
}
```

### POST question `/questions` - create new question
End point to add a new question by taking the question, answer, category, and difficulty score.

Request body example:
```
{
    "question": "Who was the first president of Kenya?",
    "answer": "Jomo Kenyatta",
    "category": 4,
    "difficulty": 1
}
```

Returns the id of the question created, total number of questions, and a success value.

Try `curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question":"Who was the first president of Kenya?", "answer":"Jomo Kenyatta", "category":4, "difficulty":1}'`

Response:
```
{
    "question_created": 29,
    "success": true,
    "totalQuestions": 20
}
```

### POST `/questions/` - search questions
Searches for specific question(s) by search term.

Takes the search term in the request body.

Request body example:
```
{
    "searchTerm": "who"
}
```

Returns the questions that match the search term, total number of questions that match, the current category string type, and a success value

Try `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'`

Response:
```
{
    "currentCategory": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Jomo Kenyatta",
            "category": 4,
            "difficulty": 1,
            "id": 28,
            "question": "Who was the first president of Kenya?"
        },
        {
            "answer": "Jomo Kenyatta",
            "category": 4,
            "difficulty": 1,
            "id": 29,
            "question": "Who was the first president of Kenya?"
        }
    ],
    "success": true,
    "totalQuestions": 5
}
```



### POST quizzes `'/quizzes'` - play the quiz game
Endpoint to get the next question to play.

Request bosy takes the previous questions which is an array of id's and quiz category which is a string of teh current category.
```
{
  'previous_questions': [12, 24, 9, 23]
  'quiz_category': 'History'
}
```

Returns a single random question in the current category, total questions available to play, the current category string type, and a success value.

Try `'curl http://127.0.0.1:5000/play'`

Response:
```
{
    "currentCategory": 4,
    "question": {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
    },
    "success": true,
    "totalQuestions": 4
}
```






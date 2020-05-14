import json
from typing import List
import csv
from datetime import datetime
from pprint import pprint as pp
from apistar import App, Route, types, validators
from bs4 import BeautifulSoup
from apistar.http import JSONResponse
from googletrans import Translator, LANGUAGES, LANGCODES
import requests


headers= 'id,created,topic,question,answer'.split(',')
questions = {}


def load_csv():
    questions.clear()
    with open('questions.csv', 'r') as f:
        csv_data = csv.DictReader(f)
        for row in csv_data:
            info = {}
            for header in headers:
                h = row[header]
                info[header]= h
            questions[row['id']] = info
    return questions


class Question(types.Type):
    id = validators.Integer(allow_null=False)
    created = validators.DateTime()
    topic = validators.Integer(allow_null=False)
    question = validators.String()
    answer = validators.String()


def list_questions(language):
    if language in LANGCODES.values():
        translator = Translator()
        return_data = [Question(id=int(question[1].get('id')),
                                created=question[1].get('created'),
                                topic=int(question[1].get('topic')),
                                question=translator.translate(question[1].get('question'),
                                                              dest=language).text,
                                answer=translator.translate(question[1].get('answer'),
                                                            dest=language).text)
                       for question in data.items()]
        return JSONResponse(return_data, status_code=200)
    else:
        return JSONResponse({}, status_code=400)

    
def test_language_translation(language, string):
    if language in LANGCODES.values():
        translator = Translator()
        return translator.translate(string, dest=language).text
    else:
        return None

    
def create_question(question):
    return JSONResponse(question, status_code=400)
    question_id = max(questions.keys()) + 1
    question.id = question_id
    question.created = datetime.now()
    questions[question_id] = question
    return JSONResponse(Question(question), status_code=201)


def post_question():
    question = Question(id=1,
                        created=datetime.now(),
                        topic=2,
                        question='Esto es una prueba de pregunta',
                        answer='Esto es una prueba de respuesta')
    q_json = {}
    q_json['id'] = question.id
    q_json['created'] = question.created
    q_json['topic'] = question.topic
    q_json['question'] = question.question
    q_json['answer'] = question.answer
    response = requests.post('http://127.0.0.1:5000/', data=q_json)
    print(response.status_code)
    return response.json()
    

def details_question():
    pass


routes = [
    Route('/{language}/', method='GET', handler=list_questions),
    Route('/', method='POST', handler=create_question),
    Route('/{language}/{question_id}/', method='GET', handler=details_question)
]

app = App(routes=routes)


if __name__ == '__main__':    
    load_csv()
    app.serve('127.0.0.1', 5000, debug=True)

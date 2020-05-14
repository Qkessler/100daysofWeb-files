import json
from typing import List
import csv
from pprint import pprint as pp
from apistar import App, Route, types, validators
from bs4 import BeautifulSoup
from apistar.http import JSONResponse
from googletrans import Translator, LANGUAGES, LANGCODES
import requests


headers= 'id,created,topic,question,answer'.split(',')
data = {}


def load_csv():
    data.clear()
    with open('questions.csv', 'r') as f:
        csv_data = csv.DictReader(f)
        for row in csv_data:
            info = {}
            for header in headers:
                h = row[header]
                info[header]= h
            data[row['id']] = info
    return data


class Question(types.Type):
    id = validators.Integer(allow_null=False)
    created = validators.DateTime()
    topic = validators.Integer(allow_null=False)
    question = validators.String()
    answer = validators.String()


def list_questions(language):
    if language in LANGCODES.values():
        translator = Translator()
        return_data = [Question(id=int(question[1].get('id')), created=question[1].get('created'),
                                topic=int(question[1].get('topic')),
                                question=translator.translate(question[1].get('question'), dest=language).text,
                                answer=translator.translate(question[1].get('answer'), dest=language).text)
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

    
def create_question():
    pass


def details_question():
    pass


routes = [
    Route('/{language}/', method='GET', handler=list_questions),
    Route('/{language}/', method='POST', handler=create_question),
    Route('/{language}/{question_id}/', method='GET', handler=details_question)
]

app = App(routes=routes)


if __name__ == '__main__':
    # print(LANGCODES)
    # print(test_language_translation('fr','This is english'))
    load_csv()
    app.serve('127.0.0.1', 5000, debug=True)

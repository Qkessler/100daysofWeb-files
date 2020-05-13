import json
from typing import List
import csv
from pprint import pprint as pp
from apistar import App, Route, types, validators
from bs4 import BeautifulSoup
from apistar.http import JSONResponse
from translate import Translator
import requests


headers= 'id,created,topic,question,answer'.split(',')
data = {}

def get_languages():
    req = requests.get('http://www.mathguide.de/info/tools/languagecode.html')
    content = req.content
    entire_file = BeautifulSoup(content, 'html.parser')
    first_table = entire_file.find_all('td')[0].find_all('tr')[1:].find_all('td')
    print(first_table)
    # languages_html = first_table[1:]
    # for l in languages_html:
    #     print(l.string)


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
    translator = Translator(to_lang=language)
    print(list(data.values())[0].get('id'))
    return_data = [Question(id=int(question[1].get('id')), created=question[1].get('created'),
                            topic=int(question[1].get('topic')),
                            question=question[1].get('question'),
                            answer=question[1].get('answer'))
                   for question in data.items()]
    return JSONResponse(return_data, status_code=200)


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
    # load_csv()
    # app.serve('127.0.0.1', 5000, debug=True)
    get_languages()

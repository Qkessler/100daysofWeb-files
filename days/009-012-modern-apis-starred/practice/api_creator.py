import json
from typing import List
import csv

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

headers = 'course_id,course_title,url,is_paid,price,num_subscribers,num_reviews,num_lectures,level,content_duration,published_timestamp,subject'.split(',')
data = {}


def load_csv():
    with open('udemy_courses.csv', 'r') as f:
        csv_data = csv.DictReader(f)
        for row in csv_data:
            for header in headers:
                 = row['id']
                data[id] = row
        

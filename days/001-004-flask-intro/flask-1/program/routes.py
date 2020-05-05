from program import app
from flask import render_template
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/beers')
def get_random_beer():
    return 'This is the beers page'


@app.context_processor
def get_context():
    return dict(date=datetime.now())

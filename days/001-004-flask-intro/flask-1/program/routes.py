from program import app
from flask import render_template
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    # context['time'] = datetime.now()
    # return render_template('index.html', context)
    return render_template('index.html')

from flask import render_template
from hms_app.main import main

@main.route('/')
def index():
    return render_template('index.html', title='Home')

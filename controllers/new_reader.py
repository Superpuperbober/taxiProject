from app import app
from flask import render_template

@app.route('/new_passanger', methods=['GET'])
def new_passanger():
    html = render_template(
        'new_reader.html',
    )
    return html

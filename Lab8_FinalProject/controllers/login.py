import flask

from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.login_model import get_user_id


@app.route('/login', methods=['get'])
def login():
    conn = get_db_connection()
    ID = get_user_id(conn, request.values.get('login'), request.values.get('password'))
    if ID:
        session['user_id'] = ID
        return flask.redirect(flask.url_for('index'))
    mistake = False
    if request.values.get('login') or request.values.get('password') and not ID:
        mistake = True
    # выводим форму
    html = render_template(
        'login.html',
        mistake=mistake
    )
    return html


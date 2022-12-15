import flask
from models.new_book_model import *
from models.book_search_model import get_author, get_genre, get_publisher
from app import app
from flask import render_template, request
from utils import get_db_connection


@app.route('/new_book', methods=['get'])
def new_book():
    conn = get_db_connection()
    if request.values.get('name'):
        create_new_book(conn, request.values.get('author'), request.values.get('genre'),
                        request.values.get('publisher'),
                        request.values.get('name'), request.values.get('year'), request.values.get('amount'))
    df_genre = get_genre(conn)
    df_author = get_author(conn)
    df_publisher = get_publisher(conn)
    conn.close()

    # генерируем результат на основе шаблона
    html = render_template(
        'new_book.html',
        genre=df_genre,
        author=df_author,
        publisher=df_publisher,
        len=len,
        print=print,
    )
    if request.values.get('name'):
        return flask.redirect('http://127.0.0.1:5000/new_book', code=302)
    else:
        return html

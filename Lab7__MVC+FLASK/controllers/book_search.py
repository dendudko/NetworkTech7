from models.book_search_model import *
from app import app
from flask import render_template, request, session
from utils import get_db_connection


@app.route('/book_search', methods=['get'])
def book_search():
    conn = get_db_connection()
    if request.values.get('book'):
        book_id = request.values.get('book')
        borrow_book(conn, book_id, session['reader_id'])
    if request.values.get('genre'):
        genre_list = request.values.getlist('genre')
    else:
        genre_list = []
    if request.values.get('author'):
        author_list = request.values.getlist('author')
    else:
        author_list = []
    if request.values.get('publisher'):
        publisher_list = request.values.getlist('publisher')
    else:
        publisher_list = []

    create_info(conn)
    df_book_info = get_book_info(conn, genre_list, author_list, publisher_list)
    df_genre = get_genre(conn)
    df_author = get_author(conn)
    df_publisher = get_publisher(conn)
    conn.close()

    # генерируем результат на основе шаблона
    html = render_template(
        'book_search.html',
        genre=df_genre,
        author=df_author,
        publisher=df_publisher,
        book_info=df_book_info,
        len=len,
        print=print,

        genre_list=genre_list,
        author_list=author_list,
        publisher_list=publisher_list
    )
    return html

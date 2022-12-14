from app import app
from flask import render_template, request, session
# import sqlite3
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, get_new_reader, return_book


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()

    # нажата кнопка Найти
    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id
    # нажата кнопка Добавить со страницы Новый читатель
    # (взять в комментарии, пока не реализована страница Новый читатель)
    elif request.values.get('new_reader'):
        html = render_template('new_reader.html')
        return html
    elif request.values.get('new_reader_fio'):
        new_reader = request.values.get('new_reader_fio')
        session['reader_id'] = int(get_new_reader(conn, new_reader))
    # нажата кнопка Не брать книгу со страницы Поиск
    elif request.values.get('return'):
        book_reader_id = int(request.values.get('return'))
        return_book(conn, book_reader_id)
    elif 'reader_id' not in session:
        session['reader_id'] = 1

    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    # выводим форму
    html = render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len
    )
    return html

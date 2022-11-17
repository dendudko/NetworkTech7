from jinja2 import Template, Environment, FileSystemLoader
import sqlite3
from book_search_model import *

# типо пользователь натыкал
genre_list = ("Детектив", "Приключения", "Роман")
author_list = ("Агата Кристи", "Жюль Верн", "Ильф И.А.,Петров Е.П.")
publisher_list = ("ДРОФА",)

conn = sqlite3.connect("library.sqlite")
df_book_info = get_book_info(conn, genre_list, author_list, publisher_list)
df_genre = get_genre(conn)
df_author = get_author(conn)
df_publisher = get_publisher(conn)
conn.close()

# создаем объект-шаблон
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('book_search_templ.html')
template.globals['len'] = len
template.globals['print'] = print

# генерируем результат на основе шаблона
result_html = template.render(
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

# создаем файл для HTML-страницы
f = open('book_search.html', 'w', encoding='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()

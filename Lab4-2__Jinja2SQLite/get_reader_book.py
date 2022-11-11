from jinja2 import Environment, FileSystemLoader
import sqlite3
from reader_book_model import get_reader, get_book_reader

# задаем id читателя, для которого формируем страницу
reader_id = 2

conn = sqlite3.connect("library.sqlite")
# выбираем записи о том, какие книги брал читатель с параметром reader_id
# столбцы назвать Название, Авторы, Дата_выдачи, Дата_сдачи
df_book_reader = get_book_reader(conn, reader_id)
# выбираем записи из таблицы reader для формирования поля со списком
df_reader = get_reader(conn)
conn.close()

# создаем объект-шаблон
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('reader_book_templ.html')
template.globals['len'] = len
# генерируем результат на основе шаблона
result_html = template.render(
    test='Дата_сдачи',
    reader_id=reader_id,
    combo_box=df_reader,
    book_reader=df_book_reader,
    len=len
)
# создаем файл для HTML-страницы
f = open('reader_book.html', 'w', encoding='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()

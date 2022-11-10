# импортируем необходимые модули
import sqlite3
from library_model import *
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('.'))
table_template = env.get_template('library_templ.html')
main_template = env.get_template('main_templ.html')
# устанавливаем соединение с базой данных (базу данных взять из ЛР 1)
con = sqlite3.connect("library.sqlite")

tables_html = ''
# Получаем все имена таблиц из базы данных
table_names = get_table_names(con)
# Генерируем все таблицы

for t in table_names:
    # генерируем результат на основе шаблона
    tables_html += table_template.render(
        table_name=t,
        table_content=get_table(con, t),
        len=len)

# Закидываем все сгенерированные таблицы на вход в main_template
# ради корректной структуры документа
result_html = main_template.render(tables=tables_html)

# создаем файл для HTML-страницы
f = open('library.html', 'w', encoding='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()
# закрываем соединение с базой данных
con.close()

import sqlite3
import pandas as pd

# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("lib.sqlite")
# открываем файл с дампом базой двнных
f_dump = open('library.db', 'r', encoding='utf-8-sig')
# читаем данные из файла
dump = f_dump.read()
# закрываем файл с дампом
f_dump.close()
# запускаем запросы
con.executescript(dump)
# сохраняем информацию в базе данных
con.commit()
# создаем курсор
cursor = con.cursor()
# # выбираем и выводим записи из таблиц author, reader
# cursor.execute("SELECT * FROM author")
# print(cursor.fetchall())
# cursor.execute("SELECT * FROM reader")
# print(cursor.fetchall())

pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False)

print('\033[1m' + 'Часть 1' + '\033[0m\n')

print('Задание 1:')
df = pd.read_sql('''SELECT genre_name as genre, count(book.book_id) as total_id, 
                    sum(book.available_numbers) as available, min(book.year_publication) as min_year
                    FROM genre JOIN book ON genre.genre_id=book.genre_id
                    group by book.genre_id ORDER BY genre_name''', con)
print(df)

print('\nЗадание 2:')
r_id = 2
df = pd.read_sql(f'''SELECT book.title, book_reader.return_date, book_reader.borrow_date, 
                    CAST (julianday(book_reader.return_date) - julianday(book_reader.borrow_date) AS INTEGER) as on_hands
                    FROM book JOIN book_reader ON
                    (book_reader.book_id=book.book_id AND book_reader.reader_id={r_id} AND 
                    book_reader.return_date IS NOT NULL)
                    ORDER BY CAST (julianday(book_reader.return_date) - julianday(book_reader.borrow_date) AS INTEGER) 
                    DESC''', con)
print(df)

print('\nЗадание 3:')
df = pd.read_sql('''SELECT genre.genre_name, count(book_reader.book_reader_id) as number_of_readers
FROM book_reader JOIN book ON book.book_id=book_reader.book_id
JOIN genre ON book.genre_id=genre.genre_id
GROUP BY genre.genre_id
HAVING count(book_reader.book_reader_id) = (SELECT count(book_reader.book_reader_id)
FROM book_reader JOIN book ON book.book_id=book_reader.book_id
JOIN genre ON book.genre_id=genre.genre_id
GROUP BY genre.genre_id ORDER BY count(book_reader.book_id) DESC LIMIT 1) 
ORDER BY genre.genre_name ASC''', con)
print(df, '\n')

print("=====" * 20)

print('\n\033[1m' + 'Часть 2' + '\033[0m\n')

print('Задание 1:')
df = pd.read_sql('''SELECT book.title AS Название, substr(trim(reader.reader_name),1,instr(trim(reader.reader_name)||' ',' ')-1) AS Читатель, book_reader.borrow_date AS Дата
FROM book, book_reader, reader WHERE
(book_reader.book_id=book.book_id AND reader.reader_id=book_reader.reader_id AND strftime('%m', book_reader.borrow_date)='10')
ORDER BY book_reader.borrow_date ASC, substr(trim(reader.reader_name),1,instr(trim(reader.reader_name)||' ',' ')-1) ASC, book.title ASC''',
                 con)
print(df)

print('\nЗадание 2+3:')
p_name = '"АСТ"'
df = pd.read_sql(f'''SELECT book.title AS Название, genre.genre_name AS Жанр, book.year_publication AS Год,
                     CASE WHEN book.year_publication<2014 THEN 'III'
                          WHEN book.year_publication BETWEEN 2014 AND 2017 THEN 'II'
                          WHEN book.year_publication>2017 THEN 'I' END AS Группа
                   FROM book
                   JOIN genre ON genre.genre_id=book.genre_id
                   JOIN publisher ON publisher.publisher_id=book.publisher_id
                   WHERE publisher.publisher_name={p_name}''', con)
print(df)

print('\nЗадание 4:')
df = pd.read_sql('''SELECT book.available_numbers AS Количество, book.title AS Название,
                        CASE WHEN count(book_reader.book_reader_id)>0 
                             THEN count(book_reader.book_reader_id)
                             ELSE 0 END
                        AS Количество_выдачи
                    FROM book
                    LEFT JOIN book_reader USING (book_id)
                    GROUP BY book.book_id
                    ORDER BY count(book_reader.book_reader_id) desc, book.title asc,
                    book.available_numbers asc''', con)
print(df)

# закрываем соединение с базой
con.close()

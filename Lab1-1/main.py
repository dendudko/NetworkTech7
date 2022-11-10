import sqlite3
import pandas as pd
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("lib.sqlite")
# создаем таблицу, если ее еще не было, заносим в нее записи
con.executescript('''
DROP TABLE IF EXISTS genre;

CREATE TABLE genre (
       genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
	   genre_name VARCHAR(30)
);

INSERT INTO genre (genre_name)  VALUES 
('Роман'),
('Приключения'),
('Детектив'),
('Лирика'),
('Фантастика'),
('Фэнтези'),
('Поэзия');

DROP TABLE IF EXISTS publisher;

CREATE TABLE publisher (
       publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
	   publisher_name VARCHAR(40)
);

INSERT INTO publisher (publisher_name)  VALUES 
('ЭКСМО'),
('ДРОФА'),
('АСТ');

DROP TABLE IF EXISTS book;

CREATE TABLE book (
      book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
	  title VARCHAR(80),
      genre_id int, 
      publisher_id INT,
      year_publication INT,
      available_numbers INT, 
      FOREIGN KEY (genre_id)  REFERENCES genre (genre_id) ON DELETE CASCADE,
      FOREIGN KEY (publisher_id)  REFERENCES publisher (publisher_id) ON DELETE CASCADE
);

INSERT INTO book(title, genre_id, publisher_id, year_publication, available_numbers)  VALUES
('Мастер и Маргарита', 1, 2, 2014, 5),
('Таинственный остров', 2, 2, 2015, 10),
('Бородино', 7, 3, 2015, 12),
('Дубровский', 1, 2, 2020, 7),
('Вокруг света за 80 дней', 2, 2, 2019, 5),
('Убийства по алфавиту', 1, 1, 2017, 9),
('Затерянный мир', 2, 1, 2020, 3),
('Герой нашего времени', 1, 3, 2017, 2),
('Смерть поэта', 7, 1, 2020, 2),
('Поэмы', 7, 3, 2019, 5);
 ''')
# сохраняем информацию в базе данных
con.commit()

cursor = con.cursor()
# cursor.execute("SELECT * FROM genre")
# result = cursor.fetchall()
#
# print(result)
# print(result[1])
# print(result[2][1])
#
# cursor.execute("SELECT * FROM genre")
# print(cursor.fetchone())

print('1. Вывести книги, количество которых принадлежит интервалу от a до b:')
cursor.execute('''
select book.book_id, book.title, genre.genre_name, book.available_numbers from book, genre
where book.available_numbers >= :a AND book.available_numbers <= :b AND book.genre_id=genre.genre_id''',
{"a": 5, "b": 7})
print(cursor.fetchall())

print('\n2. Вывести книги, название которых состоит из одного слова, и книга издана после заданного года: ')
cursor.execute('''
select book.book_id, book.title, publisher.publisher_name, book.year_publication from book, publisher
where book.year_publication >= :year AND book.title not like '% %' AND book.publisher_id=publisher.publisher_id''',
{"year": 2018})
print(cursor.fetchall())

print('\n3. Вычислить, сколько экземпляров книг каждого жанра, изданных после заданного года, представлены в библиотеке: ')
cursor.execute('''
select genre.genre_name, sum(book.available_numbers) from book, genre
where book.year_publication >= :year AND book.genre_id = genre.genre_id
group by book.genre_id''',
{"year": 2015})
print(cursor.fetchall())

print('\n4. Отобразить информацию о книгах, количество которых больше 3: ')
df = pd.read_sql('''
 SELECT
 title AS Книга,
 genre_id AS Жанр,
 publisher_id AS Издательство,
 available_numbers AS Количество
 FROM book 
 WHERE available_numbers > 3
''', con)
print('\nВ виде таблицы:')
print(df)
print('\nТолько столбец Книга:')
print(df["Книга"])
print('\n3-я строка результата запроса:')
print(df.loc[2])
print('\nКоличество строк и столбцов в результате запроса:')
print("Количество строк:", df.shape[0])
print("Количество столбцов:", df.shape[1])
print('\nНазвания столбцов:')
print(df.dtypes.index)

print('\n5. Задание про f-строки: ')
publisher_list = ("АСТ", "ДРОФА")
df = pd.read_sql(f'''
 SELECT
 book.title AS Книга,
 publisher.publisher_name AS Издательство,
 genre.genre_name AS Жанр,
 book.year_publication AS Год
 FROM book, publisher, genre
 WHERE publisher.publisher_name in {publisher_list} AND book.publisher_id = publisher.publisher_id AND book.genre_id = genre.genre_id
  AND book.year_publication between 2016 and 2019
''', con)
print(df)


con.close()

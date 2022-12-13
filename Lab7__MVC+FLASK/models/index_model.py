import pandas
import sqlite3


def get_reader(conn):
    return pandas.read_sql(
        '''
        SELECT * FROM reader
        ''', conn)


def get_book_reader(conn, reader_id):
    # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql('''
 WITH get_authors( book_id, authors_name)
 AS(
 SELECT book_id, GROUP_CONCAT(author_name)
 FROM author JOIN book_author USING(author_id)
 GROUP BY book_id
 )
 SELECT title AS Название, authors_name AS Авторы,
 borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
 book_reader_id
 FROM
 reader
 JOIN book_reader USING(reader_id)
 JOIN book USING(book_id)
 JOIN get_authors USING(book_id)
 WHERE reader.reader_id = :id
 ORDER BY 3
 ''', conn, params={"id": reader_id})


# для обработки данных о новом читателе
def get_new_reader(conn, new_reader):
    if pandas.read_sql(f'''select MAX(reader_id) from reader limit 1;''', conn).values[0][0] != \
    pandas.read_sql(f'''select MAX(reader_id) from reader
    where reader_name='{new_reader}' limit 1;''', conn).values[0][0]:
        cur = conn.cursor()
        cur.executescript(f'''
        insert into reader (reader_name) values 
        ('{new_reader}');
        ''')
        conn.commit()
        return pandas.read_sql('''SELECT MAX(reader_id) FROM reader LIMIT 1;''', conn).values[0][0]
    else:
        return pandas.read_sql('''SELECT MAX(reader_id) FROM reader LIMIT 1;''', conn).values[0][0]


def return_book(conn, book_reader_id):
    cur = conn.cursor()
    cur.executescript(f'''
    update book
    set available_numbers = available_numbers + 1
    where book_id = (select book_id from book_reader where book_reader_id={book_reader_id});
    
    update book_reader
    set return_date=DATE()
    where book_reader_id={book_reader_id};
    ''')

    return conn.commit()

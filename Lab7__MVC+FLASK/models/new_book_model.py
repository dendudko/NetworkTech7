import pandas as pd


def create_new_book(conn, author, genre, publisher, name, year, amount):
    genre_id = pd.read_sql(f'''
    select genre_id from genre
    where genre_name='{genre}';
    ''', conn).values[0][0]

    author_id = pd.read_sql(f'''
        select author_id from author
        where author_name='{author}';
    ''', conn).values[0][0]

    publisher_id = pd.read_sql(f'''
            select publisher_id from publisher
            where publisher_name='{publisher}';
    ''', conn).values[0][0]

    cur = conn.cursor()
    cur.executescript(f'''
        insert into book (title, genre_id, publisher_id, year_publication, available_numbers)
        values
        ('{name}', {genre_id}, {publisher_id}, {year}, {amount});
    ''')

    book_id = pd.read_sql('''select max(book_id) from book;''', conn).values[0][0]

    cur.executescript(f'''
        insert into book_author (book_id, author_id)
        values
        ({book_id}, {author_id});
    ''')

    conn.commit()

import pandas as pd


def get_genre(conn):
    return pd.read_sql("""
 SELECT genre_name,count(b.book_id) as counting
 FROM genre 
 join book b on genre.genre_id = b.genre_id 
 group by genre_name
 order by genre_name
 """, conn)


def get_author(conn):
    return pd.read_sql("""
 SELECT a.author_name,count(ba.book_id) as counting
 FROM book_author ba
 join author a on ba.author_id = a.author_id
 group by ba.author_id
 order by a.author_name
 """, conn)


def get_publisher(conn):
    return pd.read_sql("""
 SELECT publisher_name, count(b.book_id) 
 FROM publisher 
 join book b on publisher.publisher_id = b.publisher_id
 group by publisher_name
 order by publisher_name
 """, conn)


def get_book_info(conn, g, a, p):
    genre_list = g
    author_list = a
    publisher_list = p
    df = pd.read_sql(f"""
 select * from book_info
 where Жанр in {genre_list} and Авторы in {author_list}
  """, conn)
    return df


def create_info(conn):
    df = pd.to_sql("""
 create view if not exists book_info as
                     SELECT b.title as Название, group_concat(a.author_name)  as Авторы,
                     g.genre_name as Жанр,   p.publisher_name as Издательство, 
                     b.year_publication as ГодИздательства, b.available_numbers as Количество
                     FROM book_author
                     join book b on book_author.book_id = b.book_id
                     join author a on book_author.author_id = a.author_id
                     join genre g on b.genre_id = g.genre_id
                     join publisher p on b.publisher_id = p.publisher_id
                     group by b.title order by b.title
                     """, conn)
    return df

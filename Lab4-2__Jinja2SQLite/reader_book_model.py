import pandas as pd
import numpy as np
def get_reader(conn):
 return pd.read_sql("SELECT reader_name FROM reader", conn)

def get_book_reader(conn, id):
 df = pd.read_sql("""SELECT title as Название, group_concat(a.author_name) as Авторы,
  borrow_date as Дата_выдачи, return_date as Дата_сдачи
                    FROM book 
                    join book_author ba on book.book_id = ba.book_id
                    join author a on ba.author_id = a.author_id
                    join book_reader br on book.book_id = br.book_id 
                    where reader_id= :id
                    group by title, borrow_date order by title
                     
                    """ , conn, params={"id": id})

 df.Дата_сдачи = df.Дата_сдачи.replace('None', np.nan)
 #print(df[df['Дата_сдачи'].isnull() == True])
 df['Дата_сдачи'] = df['Дата_сдачи'].fillna('КнопкуСюда')
 return df





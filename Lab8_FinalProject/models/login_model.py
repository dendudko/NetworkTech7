import pandas


def get_user_id(conn, login=None, password=None):
    df = pandas.read_sql('''
    select IDUser, Login, Password from User
    ''', conn)
    ID = df.where(df['Login'] == login).dropna(how='any')
    ID = ID.where(ID['Password'] == password).dropna(how='any')
    if not ID.empty:
        return int(ID['IDUser'].values[0])

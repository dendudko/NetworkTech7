import pandas


def get_brands(conn):
    return pandas.read_sql(
        '''
        SELECT BrandName FROM Brand
        ''', conn)


def get_models(conn):
    return pandas.read_sql(f'''
        SELECT * FROM Model
        ''', conn)


def get_transmissions(conn):
    return pandas.read_sql('''
        SELECT TransmissionType FROM Transmission
        ''', conn)


def get_drives(conn):
    return pandas.read_sql('''
        SELECT DriveType FROM Drive
        ''', conn)


def get_fuels(conn):
    return pandas.read_sql('''
        SELECT FuelType FROM Fuel
        ''', conn)


def get_selling(conn, brand=None, model=None, min_price=None, max_price=None,
                min_year=None, max_year=None, transmission=None, drive=None,
                min_hp=None, max_hp=None):
    df = pandas.read_sql(f'''
    select Car.IDUser, BodyOrVinNumber, StateNumber, BrandName, ModelName,
    E.IDEngine, Capacity, HP, FuelType, ReleaseDate, TransmissionType, DriveType, IDEquip,
    Actuality, Price, Description, AdditionDate, ExpirationDate, CityName, IDSelling, PhoneNumber
    from Car
    join Selling S on Car.IDCar = S.IDCar
    join Engine E on E.IDEngine = Car.IDEngine
    join User U on U.IDUser = Car.IDUser
    ''', conn)
    if brand:
        df = df.where(df['BrandName'] == brand).dropna(how='any')
    if model:
        df = df.where(df['ModelName'] == model).dropna(how='any')
    if min_price:
        df = df.where(df['Price'] >= min_price).dropna(how='any')
    if max_price:
        df = df.where(df['Price'] <= max_price).dropna(how='any')
    if min_year:
        df = df.where(df['ReleaseDate'] >= min_year).dropna(how='any')
    if max_year:
        df = df.where(df['ReleaseDate'] <= max_year).dropna(how='any')
    if transmission:
        df = df.where(df['TransmissionType'] == transmission).dropna(how='any')
    if drive:
        df = df.where(df['DriveType'] == drive).dropna(how='any')
    if min_hp:
        df = df.where(df['HP'] >= min_hp).dropna(how='any')
    if max_hp:
        df = df.where(df['HP'] <= max_hp).dropna(how='any')
    return df


def remove_selling(conn, user_id, selling_id, action):
    df = pandas.read_sql('''
    select IDUser, IDSelling from Selling
    join Car C on C.IDCar = Selling.IDCar
    ''', conn)
    df = df.where(df['IDUser'] == user_id).dropna(how='any')
    df = df.where(df['IDSelling'] == float(selling_id)).dropna(how='any')
    if not df.empty:
        cursor = conn.cursor()
        cursor.executescript(f'''
        update Selling set Actuality={action}
        where IDSelling={selling_id}
        ''')
        conn.commit()

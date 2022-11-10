import sqlite3
import pandas as pd

# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("DromDB.sqlite")
pd.set_option('display.max_colwidth', None, 'display.max_rows', None,
              'display.max_columns', None, 'display.expand_frame_repr', False)
cursor = con.cursor()
con.executescript('''PRAGMA foreign_keys=on''')


def drop_tables():
    con.executescript('''
    drop table if exists Selling;
    drop table if exists Car;
    drop table if exists Drive;
    drop table if exists Engine;
    drop table if exists Fuel;
    drop table if exists Model;
    drop table if exists Brand;
    drop table if exists Transmission;
    drop table if exists User;
    drop table if exists City;
    drop table if exists Country;
    ''')
    con.commit()


def init():
    # открываем файл с дампом базы данных
    f_dump = open('DromDB.sql', 'r', encoding='utf-8-sig')
    # читаем данные из файла
    dump = f_dump.read()
    # закрываем файл с дампом
    f_dump.close()
    # запускаем запросы
    con.executescript(dump)
    # сохраняем информацию в базе данных
    con.commit()


def fill():
    # открываем файл с инсертами базы данных
    f_dump = open('DromDB_inserts.sql', 'r', encoding='utf-8-sig')
    # читаем данные из файла
    dump = f_dump.read()
    # закрываем файл с дампом
    f_dump.close()
    # запускаем запросы
    con.executescript(dump)
    # сохраняем информацию в базе данных
    con.commit()


def refill():
    drop_tables()
    init()
    fill()


def request_1_2():
    print('-----------------------------------------------------------------------------')
    print('Запрос 1 (Выбор авто и их продавцов из Уссурийска):')
    df = pd.read_sql('''select FIO as ФИО, C.BodyOrVinNumber as Номер_кузова,
    C.StateNumber as Гос_номер, CityName as Город from User
    join Car C on User.IDUser = C.IDUser
    where CityName = 'Уссурийск'
    order by FIO
    ''', con)
    print(df)

    print()

    print('Запрос 2 (Выбор всех двигателей, которые устанавливаются на а/м Toyota Vitz):')
    df = pd.read_sql('''select BodyOrVinNumber as 'Номер_кузова',
    C.IDEngine as 'Номер_двигателя', Capacity as 'Объем', HP as 'Мощность',
    FuelType as 'Тип_топлива' from Engine
    join Car C on Engine.IDEngine = C.IDEngine
    where C.BrandName = 'Toyota' and C.ModelName='Vitz'
    order by HP desc''', con)
    print(df)
    print('-----------------------------------------------------------------------------')


def request_3_4():
    print('-----------------------------------------------------------------------------')
    print('Запрос 3 (Выбор стран, автомобили из которых есть в каталоге):')
    df = pd.read_sql('''select CountryName as Страна from Brand
    group by CountryName
    order by CountryName
    ''', con)
    print(df)

    print()

    print('Запрос 4 (Выбор всех марок, модели которых сейчас продаются):')
    df = pd.read_sql('''select C.BrandName as Марка from Selling
    join Car C on C.IDCar = Selling.IDCar
    where Actuality = true
    group by C.BrandName
    ''', con)
    print(df)
    print('-----------------------------------------------------------------------------')


def request_5_6():
    print('-----------------------------------------------------------------------------')
    # # Запрос в правильном виде?
    # print('Запрос 5 (Выбор страны, у которой больше всего марок):')
    # df = pd.read_sql('''
    # with nt1 as (select CountryName, count(CountryName) as count from Brand
    # group by CountryName),
    # nt2 as (select max(count) as max from nt1)
    # select nt1.CountryName, nt1.count from nt1, nt2
    # where nt1.count = nt2.max
    # group by nt1.CountryName
    # ''', con)
    # print(df)

    print('Запрос 5 (Выбор страны, у которой больше всего марок):')
    df = pd.read_sql('''select CountryName as Страна, max(count) as Количество_марок from
        (select Brand.CountryName, count(Brand.CountryName) as count from Brand
        group by Brand.CountryName)
        ''', con)
    print(df)

    print()

    print('Запрос 6 (Выбор марки, у которой меньше всего моделей):')
    df = pd.read_sql('''select BrandName as Марка, min(count) as Количество_моделей from 
        (select Model.BrandName, count(Model.ModelName) as count from Model
        group by Model.BrandName)
        ''', con)
    print(df)
    print('-----------------------------------------------------------------------------')


def request_7_8():
    print('-----------------------------------------------------------------------------')
    print('Запрос 7 (Изменяем название топлива: Дизель -> Солярка):')
    cursor.executescript('''update Fuel 
    set FuelType = 'Солярка'
    where FuelType = 'Дизель'
    ''')
    df = pd.read_sql('''select * from Fuel''', con)
    print(df)
    print()
    df = pd.read_sql('''select * from Engine''', con)
    print(df)

    print()

    print('Запрос 8 (Удаляем из БД неиспользуемые страны):')
    cursor.executescript('''delete from Country 
        where CountryName not in (select CountryName from Brand)
        ''')
    df = pd.read_sql('''select * from Country order by CountryName''', con)
    print(df)
    print()
    print('После всего этого безобразия восстанавливаем БД...')
    refill()
    print('-----------------------------------------------------------------------------')


# Main
# refill() #После первого запуска эту строку можно закомментировать
request_1_2()
request_3_4()
request_5_6()
request_7_8()

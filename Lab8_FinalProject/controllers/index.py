import pandas

from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_brands, get_models, \
    get_transmissions, get_drives, get_selling


def check_min_max(min_v, max_v):
    if min_v > max_v:
        a = min_v
        min_v = max_v
        max_v = a
    return min_v, max_v


@app.route('/', methods=['get'])
def index():

    session['user_id'] = 1

    conn = get_db_connection()

    brand = None
    df_brands = get_brands(conn)
    if request.values.get('brand'):
        brand = request.values.get('brand')

    model = None
    df_models = get_models(conn)
    if request.values.get('model'):
        model = request.values.get('model')

    min_price = None
    max_price = None
    if request.values.get('minprice'):
        min_price = int(request.values.get('minprice'))
    if request.values.get('maxprice'):
        max_price = int(request.values.get('maxprice'))
    if min_price and max_price:
        min_price, max_price = check_min_max(min_price, max_price)

    min_year = None
    max_year = None
    if request.values.get('minyear'):
        min_year = int(request.values.get('minyear'))
    if request.values.get('maxyear'):
        max_year = int(request.values.get('maxyear'))
    if min_year and max_year:
        min_year, max_year = check_min_max(min_year, max_year)

    transmission = None
    df_transmissions = get_transmissions(conn)
    if request.values.get('transmission'):
        transmission = request.values.get('transmission')

    drive = None
    df_drives = get_drives(conn)
    if request.values.get('drive'):
        drive = request.values.get('drive')

    df_selling = get_selling(conn, brand, model, min_price, max_price,
                             min_year, max_year, transmission, drive)

    # выводим форму
    html = render_template(
        'index.html',
        user_id=session['user_id'],
        brand=brand,
        model=model,
        brands=df_brands,
        models=df_models,
        min_price=min_price,
        max_price=max_price,
        min_year=min_year,
        max_year=max_year,
        transmissions=df_transmissions,
        transmission=transmission,
        drives=df_drives,
        drive=drive,
        df_selling=df_selling,
        iterrows=pandas.DataFrame.iterrows,
        len=len,
        str=str,
        int=int
    )
    return html

import pandas as pd
import sqlite3
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import os
import yaml
from .format_table import *
from .auto_data import get_auto_data

config = yaml.safe_load(open("C:/Users/User/Desktop/Programming/Spb_cars_sales/config/config.yaml"))['database']


def format_columns(data):
    split_auto_engine(data)
    get_price(data)
    get_mileage(data)
    get_owners(data)
    get_brand_model(data)
    get_guarantee_date(data)

    new_data = data.astype({'Engine_displacement': 'float64', 'Price': 'int64',
                            'Capacity': 'int64', 'auto_mileage': 'int64', 'owners': 'int64'})

    new_data = new_data.drop(columns=['htpp', 'emp', 'web', 'city', 'type', 'em2',
                                      'auto_price', 'auto_owners', 'auto_engine', 'Currency', '1',
                                      'auto_guarantee'])
    return new_data


def carcase_type(data):
    data['carcase'] = 0
    suv = ['Внедорожник 3 дв.', 'Внедорожник 3 дв. Urban', 'Внедорожник 5 дв.', 'Внедорожник 5 дв. Cooper S',
           'Внедорожник 5 дв. Coupe', 'Внедорожник 5 дв. Grand', 'Внедорожник 5 дв. JCW', 'Внедорожник 5 дв. L',
           'Внедорожник 5 дв. Long', 'Внедорожник 5 дв. Prime', 'Внедорожник 5 дв. SRT']

    sedan = ['Седан', 'Седан Gran Coupe', 'Седан Long', 'Седан Sport', 'Седан Stepway']

    hatchback = ['Хэтчбек 3 дв.', 'Хэтчбек 3 дв. GTC', 'Хэтчбек 3 дв. JCW', 'Хэтчбек 5 дв.',
                 'Хэтчбек 5 дв. Cooper S', 'Хэтчбек 5 дв. Cross', 'Хэтчбек 5 дв. Sportback',
                 'Хэтчбек 5 дв. Stepway', 'Хэтчбек 5 дв. X', 'Хэтчбек 5 дв. X-Line']

    liftback = ['Лифтбек', 'Лифтбек Gran Coupe', 'Лифтбек Gran Turismo', 'Лифтбек Sportback']

    station_wagon = ['Универсал 5 дв.', 'Универсал 5 дв. All-Terrain', 'Универсал 5 дв. SW', 'Универсал 5 дв. SW Cross',
                     'Универсал 5 дв. Scout', 'Универсал 5 дв. Cross']

    minivan = ['Компактвэн', 'Компактвэн Freetrack', 'Компактвэн Grand', 'Компактвэн Life',
               'Минивэн L', 'Минивэн L2', 'Минивэн', 'Минивэн LWB', 'Минивэн M', 'Минивэн SWB']

    data['carcase'] = data.auto_carcase.apply(lambda x : 'SUV' if x in suv
                                              else 'sedan' if x in sedan
                                              else 'hatchback' if x in hatchback
                                              else 'liftback' if x in liftback
                                              else 'station_wagon' if x in station_wagon
                                              else 'minivan' if x in minivan
                                              else 'other')


def encode_cols(data):
    ord_enc = OrdinalEncoder()
    data["auto_carcase_enc"] = ord_enc.fit_transform(data[["carcase"]])
    data["auto_brand_enc"] = ord_enc.fit_transform(data[["brand"]])
    data["auto_transmission_enc"] = ord_enc.fit_transform(data[["auto_transmission"]])
    data["auto_drive_unit_enc"] = ord_enc.fit_transform(data[["auto_drive_unit"]])


def encode_columns(data):
    carcase_type(data)
    encode_cols(data)


def remove_extreme_values(data):
    new_data = data.drop(data[data['Price'] > 6000000].index, axis=0)
    new_data = new_data.drop(data[data['Price'] < 400000].index, axis=0)
    return new_data


def drop_columns(data):
    new_data = data[['Price', 'auto_year', 'Capacity', 'guarantee_year',
                    'auto_carcase', 'auto_carcase_enc', 'brand', 'auto_brand_enc',
                     'auto_transmission', 'auto_transmission_enc', 'auto_drive_unit', 'auto_drive_unit_enc']]

    return new_data


def create_db():
    if config['update_csv']:
        print('Collecting information...')
        get_auto_data()
    old_data = pd.read_csv(config['DIR'] + config['CSV_FILE'], sep=';')
    df = format_columns(old_data)
    encode_columns(df)
    df = remove_extreme_values(df)
    new_data = drop_columns(df)

    conn = sqlite3.connect(config['DIR'] + config['DB_NAME'])
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cars '
              '(Price, auto_year, Capacity, guarantee_year,'
              'auto_carcase_enc, auto_brand_enc,'
              'auto_transmission_enc, auto_drive_unit_enc)')
    new_data.to_sql('cars', conn, if_exists='replace', index=False)
    c.close()

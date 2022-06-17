import os
import pandas as pd
import sqlite3
from flask import Flask, render_template
from flask_cors import cross_origin
import joblib
import yaml

import train
from forms import SelectAutoCharacteristics

config = yaml.safe_load(open("C:/Users/User/Desktop/Programming/Spb_cars_sales/config/config.yaml"))
model_name = config['train']['model_name']
config_db = config['database']

auto_brand_enc = dir()
auto_carcase_enc = dir()
auto_transmission_enc = dir()
auto_drive_unit_enc = dir()


def get_encoded_values():
    try:
        global auto_brand_enc
        global auto_carcase_enc
        global auto_transmission_enc
        global auto_drive_unit_enc

        conn = sqlite3.connect(config_db['DIR'] + config_db['DB_NAME'])
        data = pd.read_sql_query('SELECT * FROM cars', conn)
        data_brands = pd.DataFrame(data, columns=['brand', 'auto_brand_enc']).drop_duplicates().reset_index()
        data_carcase = pd.DataFrame(data, columns=['auto_carcase', 'auto_carcase_enc']).drop_duplicates().reset_index()
        data_transmission = pd.DataFrame(data, columns=['auto_transmission', 'auto_transmission_enc']).drop_duplicates().reset_index()
        data_drive_unit = pd.DataFrame(data, columns=['auto_drive_unit', 'auto_drive_unit_enc']).drop_duplicates().reset_index()

        auto_brand_enc = dict(zip(data_brands.brand, data_brands.auto_brand_enc))
        auto_carcase_enc = dict(zip(data_carcase.auto_carcase, data_carcase.auto_carcase_enc))
        auto_transmission_enc = dict(zip(data_transmission.auto_transmission, data_transmission.auto_transmission_enc))
        auto_drive_unit_enc = dict(zip(data_drive_unit.auto_drive_unit, data_drive_unit.auto_drive_unit_enc))

        conn.close()

    except Exception as e:
        print(e)
        return 1
    return 0


try:
    model = joblib.load(model_name)
except Exception as e:
    print(e)
    print("Creating new model...")
    test.get_prediction_model()

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
@cross_origin()
def home():
    form = SelectAutoCharacteristics()
    form.brand.choices = sorted(list(auto_brand_enc.keys()))
    form.carcase.choices = sorted(list(auto_carcase_enc.keys()))
    form.transmission.choices = sorted(list(auto_transmission_enc.keys()))
    form.drive_unit.choices = sorted(list(auto_drive_unit_enc.keys()))
    return render_template('index.html', form=form)


@app.route('/result', methods=['GET', 'POST'])
@cross_origin()
def result():
    form = SelectAutoCharacteristics()
    form.brand.choices = sorted(list(auto_brand_enc.keys()))
    form.carcase.choices = sorted(list(auto_carcase_enc.keys()))
    form.transmission.choices = sorted(list(auto_transmission_enc.keys()))
    form.drive_unit.choices = sorted(list(auto_drive_unit_enc.keys()))
    if form.submit.data:
        auto_year = form.year.data
        capacity = form.engine_capacity.data
        guarantee_year = form.guarantee.data
        carcase = auto_carcase_enc[form.carcase.data]
        drive_unit = auto_drive_unit_enc[form.drive_unit.data]
        transmission = auto_transmission_enc[form.transmission.data]
        auto_brand = auto_brand_enc[form.brand.data]

        output = model.predict([[auto_year,
                                 capacity,
                                 guarantee_year,
                                 carcase,
                                 auto_brand,
                                 transmission,
                                 drive_unit]], )

        output = output[0]

        str_out = f'Brand: {form.brand.data}<br />' \
                  f'Carcase: {form.carcase.data}<br />' \
                  f'Year of manufacture: {auto_year}<br />' \
                  f'Engine capacity: {capacity}<br />' \
                  f'Drive unit: {form.drive_unit.data}<br />' \
                  f'Transmission: {form.transmission.data}<br />' \
                  f'End of guarantee: {guarantee_year}<br />' \
                  f'Estimated car price as of June 2022: {output: 10,.2f} RUB'

        return (render_template('index.html',
                                form=form,
                                prediction=str_out))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    if config['app']['get_prediction_model']:
        print("Creating model...")
        train.get_prediction_model()
    if get_encoded_values() == 0:
        app.run(debug=True)

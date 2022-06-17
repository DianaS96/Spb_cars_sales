from src import etl
import sqlite3
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error

import lightgbm

import yaml

import pickle
import joblib

config = yaml.safe_load(open("C:/Users/User/Desktop/Programming/Spb_cars_sales/config/config.yaml"))
config_db = config['database']
test_size = config['train']['test_size']
random_state = config['train']['random_state']
max_depth = config['train']['max_depth']
n_estimators = config['train']['n_estimators']
learning_rate = config['train']['learning_rate']


def fit(data):
    y = data['Price']
    x = data.drop(columns=['Price'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

    lgbm_reg = lightgbm.LGBMRegressor(max_depth=max_depth,
                                      n_estimators=n_estimators,
                                      learning_rate=learning_rate,
                                      random_state=random_state).fit(x_train, y_train)

    prediction = lgbm_reg.predict(x_test)

    r2_score = metrics.r2_score(y_test, prediction)
    mse = mean_squared_error(y_test, prediction)
    lgbm_rmse = np.sqrt(mse)
    lgbm_mae = mean_absolute_error(y_test, prediction)
    print(f'r2score: {r2_score:.3f}')
    print(f'lgbm_rmse: {lgbm_rmse:.3f}')
    print(f'lgbm_mae: {lgbm_mae:.3f}')

    joblib.dump(lgbm_reg, config['train']['model_name'])


def get_prediction_model():
    if config_db['create_db']:
        print("Creating database...")
        etl.create_db()
    try:
        conn = sqlite3.connect(config_db['DIR'] + config_db['DB_NAME'])
        data = pd.read_sql_query('SELECT * FROM cars', conn)
        df = pd.DataFrame(data, columns=['Price', 'auto_year', 'Capacity', 'guarantee_year',
                                         'auto_carcase_enc', 'auto_brand_enc',
                                         'auto_transmission_enc', 'auto_drive_unit_enc'])
        conn.close()
        fit(df)
    except Exception as e:
        print(e)
        return 1
    return


import pandas as pd
from flask import Flask, request, render_template
import pickle
from flask_cors import cross_origin
import sklearn
import joblib

model = joblib.load('lgb.pkl')
app = Flask(__name__)

@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
@cross_origin()
def result():
    if request.method =='POST':
        auto_carcase = request.form['Carcase']
        carcase = 0
        if (auto_carcase == 'SUV'):
            carcase = 1
        elif (auto_carcase == 'Sedan'):
            carcase = 2
        elif (auto_carcase == 'Hatchback'):
            carcase = 3
        elif (auto_carcase == 'Liftback'):
            carcase = 4
        elif (auto_carcase == 'Station_wagon'):
            carcase = 5
        elif (auto_carcase == 'Station_wagon'):
            carcase = 6

        auto_year = request.form['year']

        Capacity = request.form['Capacity']

        auto_drive_unit = request.form['auto_drive_unit']
        drive_unit = 0
        if (auto_drive_unit == 'four-wheel-drive'):
            drive_unit = 0
        elif (auto_drive_unit == 'front-wheel-drive'):
            drive_unit = 1
        elif (auto_drive_unit == 'Rear-wheel-drive'):
            drive_unit = 2

        auto_transmission = request.form['Transmission']
        transmission = 4
        if (auto_transmission == 'Automatic'):
            transmission = 1
        if (auto_transmission == 'Manual'):
            transmission = 2
        if (auto_transmission == 'Robotic'):
            transmission = 3

        guarantee_year = request.form['guarantee']

        brand = request.form['Brand']
        auto_brand = 0
        if (brand == 'alfa-romeo'):
            auto_brand = 0
        elif (brand == 'audi'):
            auto_brand = 1
        elif (brand == 'bentley'):
            auto_brand = 2
        elif (brand == 'bmw'):
            auto_brand = 3
        elif (brand == 'cadillac'):
            auto_brand = 4
        elif (brand == 'chery'):
            auto_brand = 5
        elif (brand == 'chevrolet'):
            auto_brand = 6
        elif (brand == 'chrysler'):
            auto_brand = 7
        elif (brand == 'citroen'):
            auto_brand = 8
        elif (brand == 'datsun'):
            auto_brand = 9
        elif (brand == 'dodge'):
            auto_brand = 10
        elif (brand == 'dongfeng'):
            auto_brand = 11
        elif (brand == 'fiat'):
            auto_brand = 12
        elif (brand == 'ford'):
            auto_brand = 13
        elif (brand == 'geely'):
            auto_brand = 14
        elif (brand == 'genesis'):
            auto_brand = 15
        elif (brand == 'haval'):
            auto_brand = 16
        elif (brand == 'honda'):
            auto_brand = 17
        elif (brand == 'hyundai'):
            auto_brand = 18
        elif (brand == 'infiniti'):
            auto_brand = 19
        elif (brand == 'izh'):
            auto_brand = 20
        elif (brand == 'jaguar'):
            auto_brand = 21
        elif (brand == 'jeep'):
            auto_brand = 22
        elif (brand == 'kia'):
            auto_brand = 23
        elif (brand == 'lada--vaz-'):
            auto_brand = 24
        elif (brand == 'land-rover'):
            auto_brand = 25
        elif (brand == 'lexus'):
            auto_brand = 26
        elif (brand == 'lifan'):
            auto_brand = 27
        elif (brand == 'maserati'):
            auto_brand = 28
        elif (brand == 'mazda'):
            auto_brand = 29
        elif (brand == 'mercedes'):
            auto_brand = 30
        elif (brand == 'mini'):
            auto_brand = 31
        elif (brand == 'mitsubishi'):
            auto_brand = 32
        elif (brand == 'nissan'):
            auto_brand = 33
        elif (brand == 'opel'):
            auto_brand = 34
        elif (brand == 'peugeot'):
            auto_brand = 35
        elif (brand == 'pontiac'):
            auto_brand = 36
        elif (brand == 'porsche'):
            auto_brand = 37
        elif (brand == 'renault'):
            auto_brand = 38
        elif (brand == 'saab'):
            auto_brand = 39
        elif (brand == 'seat'):
            auto_brand = 40
        elif (brand == 'skoda'):
            auto_brand = 41
        elif (brand == 'ssangyong'):
            auto_brand = 42
        elif (brand == 'subaru'):
            auto_brand = 43
        elif (brand == 'suzuki'):
            auto_brand = 44
        elif (brand == 'toyota'):
            auto_brand = 45
        elif (brand == 'uaz'):
            auto_brand = 46
        elif (brand == 'volkswagen'):
            auto_brand = 47
        elif (brand == 'volvo'):
            auto_brand = 48

        output = model.predict([[auto_year,
                                 Capacity,
                                 guarantee_year,
                                 carcase,
                                 drive_unit,
                                 transmission,
                                 auto_brand]])

        output = output[0]

        str_out = f'Brand: {brand}<br />'\
                  f'Carcase: {auto_carcase}<br />'\
                  f'Year of manufacture: {auto_year}<br />'\
                  f'Engine capacity: {Capacity}<br />'\
                  f'Drive unit: {auto_drive_unit}<br />'\
                  f'Transmission: {auto_transmission}<br />'\
                  f'End of guarantee: {guarantee_year}<br />'\
                  f'Estimated car price as of 19/02/2022: {output: 10,.2f} RUB'

        return (render_template('index.html',
                                prediction=str_out))


if __name__ == '__main__':
    app.run(debug=True)

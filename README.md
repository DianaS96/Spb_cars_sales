# Car price prediction (spb market of used cars)

## What I did
1) First, I scraped data on cars from the website https://rolf-probeg.ru/spb/cars/ (pls, see **auto_data.py** file in **src** folder).
2) Second, I performed data cleaning, EDA and converted categorical data to numerical data (pls, see **etl.py** file in **src** folder. ETL was also performed in **auto_rolf_june.ipynb** file).
3) The next step was model selection. Initially I used LinearRegression, but it gave unsatisfactory result. So I tried RandomForestRegressor tuning with RandomizedSearchCV,  GradientBoostingRegressor, LightGBM, CatBoostRegressor, XGboost. <br>
I chose LightGBM as this model is the fastest one and has pretty high accuracy. (pls, see auto_rolf.ipynb file) <br>

Pls, find below model's metrics:

| Metrics  | Score |
| ------------- | ------------- |
| r^2 |  0.892 |
| rmse |  347 296.14 RUB |
| mae |  243 047.57 RUB |

4) The final step was creating GUI with HTML and CSS.
### You can see example in video below.
https://user-images.githubusercontent.com/81222865/174400827-fe78b961-5f8e-4fb5-9561-d3e19dab6ca0.mp4

## Usage

* Clone this repo.
* Install the required packages (see requirements.txt).
* Run **`flask run`** or **`app.py`**.


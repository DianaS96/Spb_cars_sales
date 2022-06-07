# Car price prediction (spb market of used cars)

## What I did
1) First, I scraped data on cars from the website https://rolf-probeg.ru/spb/cars/ (pls, see auto_data.py file).
2) Second, I performed data cleaning, EDA and converted categorical data to numerical data (pls, see auto_rolf.ipynb file).
3) The next step was model selection. Initially I used LinearRegression, but it gave unsatisfactory result. So I tried RandomForestRegressor tuning with RandomizedSearchCV,  GradientBoostingRegressor, LightGBM, CatBoostRegressor, XGboost. <br>
I chose LightGBM as this model is the fastest one and has pretty high accuracy. (pls, see auto_rolf.ipynb file)
5) The final step was creating GUI with HTML and CSS.
### You can see example in video below.
https://user-images.githubusercontent.com/81222865/159007870-9039915b-e20c-4457-8836-82bd047a4723.mp4

## Usage

* Clone this repo.
* Install the required packages (see requirements.txt).
* Run **`flask run`** or **`app.py`**.

*Prediction of estimated car price is made based on sample data collected before 24/02/2022.<br/>
The events of 24/02/2022 led to supply reduction and increase in production cost, which resulted in car prices increase.*

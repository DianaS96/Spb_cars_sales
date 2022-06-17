import numpy as np

def get_price(data):
    """
    Format Price column
    :param data: DataFrame with autos info
    """
    data[['Price', 'Currency']] = data.auto_price.str.split(pat='                    ', expand=True)
    data.Price = data.Price.str.replace(' ', '')


def get_owners(data):
    """
    Create and format owners column
    :param data: DataFrame with autos info
    """
    data[['owners', '1']] = data['auto_owners'].apply(str).str.split(pat="                ", expand=True)
    data['owners'] = [x for x in data['owners']]


def get_mileage(data):
    """
    Format auto_mileage column
    :param data: DataFrame with autos info
    """
    data['auto_mileage'] = data['auto_mileage'].apply(str).str.replace(' км', '').apply(str).str.replace(' ', '')


def get_brand_model(data):
    """
    Create column brand_model
    :param data: DataFrame with autos info
    """
    data[['htpp', 'emp', 'web', 'city', 'type', 'brand', 'model', 'id', 'em2']] = data['link'].str.split(pat='/',
                                                                                                         expand=True)
    data['brand_model'] = data['brand'] + "_" + data['model']


def get_guarantee_date(data):
    """
    Create columns with guarantee period expiration date
    :param data: DataFrame with autos info
    :return: new DataFrame
    """
    data[['emp', 'guarantee_date']] = data['auto_guarantee'].str.split(pat='                  ', expand=True)
    data[['guarantee_month', 'guarantee_year']] = data['guarantee_date'].str.split(pat='.', expand=True)
    data['guarantee_year'] = [0 if x is None else x for x in data['guarantee_year']]
    data['guarantee_month'] = [0 if x is None else x for x in data['guarantee_month']]

    data.guarantee_month = data.guarantee_month.fillna(0)
    data.guarantee_year = data.guarantee_year.fillna(0)
    data.guarantee_date = data.guarantee_date.fillna(0)

    data.guarantee_year = data.guarantee_year.astype(np.float).astype("int64")
    data.guarantee_month = data.guarantee_month.astype(np.float).astype("int64")
    data.guarantee_date = data.guarantee_date.astype(np.float).astype("int64")
    data.auto_year = data.auto_year.astype(np.float).astype("int64")

    return data


def split_auto_engine(data):
    """
    Create columns with Engine_displacement, Capacity and Fuel data
    :param data: DataFrame with autos info
    """
    data[['Engine_displacement', 'Capacity', 'Fuel']] = data['auto_engine'].str.split(pat='/\n', expand=True)
    data.Engine_displacement = data.Engine_displacement.apply(str).str.replace(' л ', '')
    data.Capacity = data.Capacity.apply(str).str.replace(' л.с.', '')
    data.Fuel = data.Fuel.apply(str).str.strip()

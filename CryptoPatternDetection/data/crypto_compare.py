# library
import numpy as np
import pandas as pd

import requests
from datetime import datetime

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout

from sklearn.preprocessing import StandardScaler
# from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns

# pretty printing of pandas dataframe
# pd.set_option('expand_frame_repr', False)
plt.style.use('default')

key = 'dfa3e8f0e629d438b183f88b44be15b16d5c2ef8664e12000f658a996e5656f9'

def get_hist_data(from_sym='BTC', to_sym='USD', timeframe='day', limit=2000,
                  aggregation=1, exchange='', toTs=None, data_type='price'):
    url = None

    if data_type == 'price':
        url = 'https://min-api.cryptocompare.com/data/v2/histo'
        parameters = {'fsym': from_sym,
                      'tsym': to_sym,
                      'limit': limit,
                      'api_key': key,
                      'aggregate': aggregation}
    elif data_type == 'blockchain':
        url = 'https://min-api.cryptocompare.com/data/blockchain/histo/'
        parameters = {'fsym': from_sym,
                      'tsym': to_sym,
                      'limit': limit,
                      'api_key': key,
                      'aggregate': aggregation}
    elif data_type == 'social':
        url = 'https://min-api.cryptocompare.com/data/social/coin/histo/'
        parameters = {
                      'limit': limit,
                      'api_key': key}

    url += timeframe



    if toTs:
        parameters['toTs'] = toTs
    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange

    print('baseurl: ', url)
    print('timeframe: ', timeframe)
    print('parameters: ', parameters)

    # response comes as json
    response = requests.get(url, params=parameters)
    if data_type != 'social':
        data = response.json()['Data']['Data']
    else:
        data = response.json()['Data']

    return data


def data_to_dataframe(data):
    # data from json is in array of dictionaries
    df = pd.DataFrame.from_dict(data)

    # time is stored as an epoch, we need normal dates
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    # print(df.tail())

    return df


def plot_data(df, cryptocurrency, target_currency):
    # got his warning because combining matplotlib
    # and time in pandas converted from epoch to normal date
    # To register the converters:
    # 	>>> from pandas.plotting import register_matplotlib_converters
    # 	>>> register_matplotlib_converters()
    #  warnings.warn(msg, FutureWarning)

    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()

    plt.figure(figsize=(15, 5))
    plt.title('{} / {} price data'.format(cryptocurrency, target_currency))
    plt.plot(df.index, df.close)
    plt.legend()
    plt.show()

    return None


def get_timeseries_history(pair, start_date, end_date, timeframe, data_type ='price'):
    cryptocurrency, target_currency = pair.split('/')

    ed = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
    sd = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())

    df_all = None

    if timeframe == 'day':
        delta_ed = 60 * 60 * 24
    elif timeframe == 'hour':
        delta_ed = 60 * 60
    elif timeframe == 'minute':
        delta_ed = 60

    while sd < ed - 2000 * delta_ed:
        data = get_hist_data(cryptocurrency, target_currency, timeframe, limit=2000, toTs=ed, data_type = data_type)
        ed = ed - 2000 * delta_ed
        ed = pd.to_datetime(ed, unit='s').to_pydatetime().timestamp()
        df = data_to_dataframe(data)
        df_all = df if df_all is None else pd.concat([df, df_all])

    while sd < ed:
        limit_num = int((ed-sd)/delta_ed)
        data = get_hist_data(cryptocurrency, target_currency, timeframe, limit=limit_num, toTs=ed, data_type = data_type)
        ed = ed - 2000 * delta_ed
        ed = pd.to_datetime(ed, unit='s').to_pydatetime().timestamp()
        df = data_to_dataframe(data)
        df_all = df if df_all is None else pd.concat([df, df_all])

    #plot_data(df_all, cryptocurrency, target_currency)
    return df_all





if __name__ == '__main__':
    df = get_timeseries_history('ETH/USD', '2021-12-09', '2022-02-07', 'day', data_type='blockchain')
    df = get_timeseries_history('BTC/USD', '2021-12-09', '2022-02-07', 'day', data_type='blockchain')
    #df.plot(y='hashrate')
    df = get_timeseries_history('ETH/USD', '2021-12-09', '2022-02-07', 'hour', data_type='social')

    df = get_timeseries_history('ETH/USD', '2021-12-09', '2022-02-07', 'hour')
    df.to_csv('./csv/ETHUSD_history.csv')
    print(df.head())
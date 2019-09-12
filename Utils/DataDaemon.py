from apscheduler.schedulers.blocking import BlockingScheduler
from configparser import ConfigParser
import config
import os
import requests
import pandas as pd
import time
import io


class DataDaemon:
    def __init__(self):
        self.URL = "https://www.alphavantage.co/query?"
        self.path = config.PATH

        self.headers = {
            'apikey': config.APIKEY,
            'function': 'TIME_SERIES_DAILY',
            'outputsize': 'full',
            'datatype': 'csv'
        }

    def get_alphavantage_data(self, ticker):
        headers = self.headers
        headers['symbol'] = ticker
        filename = self.path + 'Data' + os.sep + 'AlphaVantage' + os.sep + ticker + '.csv'
        data = requests.get(self.URL, self.headers)
        data.raw.decode_content = True
        try:
            df = pd.read_csv(filename)
        except FileNotFoundError:
            pass
        if data.status_code == 200:
            data = pd.read_csv(io.StringIO(data.text))
        try:
            if 'data' in locals() and 'df' in locals():
                data.merge(df, how='outer', on='timestamp')
                del df
        except:
            print(df.head()) 
            print(data.head())
        
        data.to_csv(filename)
        del data


@sched.scheduled_job('cron', hour=4)
def update():
    daemon = DataDaemon()
    path = config.PATH
    last_updated = config.LAST_UPDATED
    tickers = pd.read_csv(path + 'Data' + os.sep + 'EquityLists' 
                          + os.sep + 'NYSEcompanylist.csv')
    tickers = tickers.merge(pd.read_csv(path + 'Data' + os.sep + 'EquityLists' 
                                        + os.sep + 'NASDAQcompanylist.csv'), how = 'outer')
    if last_updated == '':
        index = 0
    else:
        index = tickers[tickers['Symbol'] == last_updated].index[0]
    tickers = tickers.iloc[index:index+500]
    i=0
    for _, row in tickers.iterrows():
        daemon.get_alphavantage_data(row['Symbol'])
        time.sleep(12)
        i += 1
        print(str(i) + ' ' + row['Symbol'])
    

if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='EST')
    scheduler.start()
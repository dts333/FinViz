from apscheduler.schedulers.blocking import BlockingScheduler
from Configs import config
import requests
import pandas as pd
import io


class DataDaemon:
    def __init__(self):
        self.URL = "https://www.alphavantage.co/query?"
        self.last_updated = config.LAST_UPDATED

        self.headers = {
            'apikey': config.ALPHAVANTAGE_APIKEY,
            'function': 'TIME_SERIES_DAILY',
            'outputsize': 'full',
            'datatype': 'csv'
        }

    def gather_alphavantage_data(self, ticker):
        headers = self.headers
        headers['symbol'] = ticker
        data = requests.get(self.URL, self.headers)
        data.raw.decode_content = True
        #with open(path + 'Data\\AlphaVantage\\' + ticker + '.csv', 'wb') as file:
        #    for chunk in data:
        #        file.write(chunk)
        try:
            df = pd.read_csv(path + 'Data\\AlphaVantage\\' + ticker + '.csv')
        except FileNotFoundError:
            pass
        


@sched.scheduled_job('cron', hour=4)
def update():
    daemon = DataDaemon()
    path = config.PATH
    tickers = pd.read_csv(path + "Data\\EquityLists\\NYSEcompanylist.csv")
    tickers = tickers.merge(pd.read_csv(path + "Data\\EquityLists\\NASDAQcompanylist.csv"))


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='EST')
    scheduler.start()
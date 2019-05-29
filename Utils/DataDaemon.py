import Configs.config as config
import requests
import pandas as pd
import io


class DataDaemon:
    def __init__(self):
        self.URL = "https://www.alphavantage.co/query?"

        self.headers = {
            'apikey': config.ALPHAVANTAGE_APIKEY,
            'function': 'TIME_SERIES_DAILY',
            'outputsize': 'full',
            'datatype': 'csv'
        }

    #AlphaVantage is limiting me to 500 API calls/day - not really what I want
    def gather_alphavantage_data(self):
        headers = self.headers
        path = config.PATH
        tickers = pd.read_csv(path + "Data\\EquityLists\\NYSEcompanylist.csv")
        tickers = tickers.merge(pd.read_csv(path + "Data\\EquityLists\\NASDAQcompanylist.csv"))

        for _, row in tickers.iterrows():
            ticker = row["Symbol"]
            headers['symbol'] = ticker
            data = requests.get(self.URL, self.headers)
            data.raw.decode_content = True
            with open(path + 'Data\\AlphaVantage\\' + ticker + '.csv', 'wb') as file:
                for chunk in data:
                    file.write(chunk)


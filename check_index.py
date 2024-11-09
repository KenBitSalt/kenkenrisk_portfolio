import yfinance as yf
#import tushare as ts
import datetime
import pandas as pd

default_data_api = "tushare"
tushare_token = "88496aa09c93288465c2695e8ebf44f51442e0c7d3756d6485df3baa"

class index:
    def __init__(self, ticker, market, method = "undefined", date = "today"):
        self.ticker = ticker
        self.market = market
        if method == "undefined":
            #default data api
            if market == "U.S.":
                self.method = "yfinance"
            elif market == "China-A":
                self.method = default_data_api
        if date == "today":
            self.date = datetime.datetime.now().strftime('%Y-%m-%d')

    def get_weight(self):
        if self.method == "yfinance":
            pass

#index_1 = index("SPY","U.S.")
#index_1.get_weight()
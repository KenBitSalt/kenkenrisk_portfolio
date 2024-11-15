import tushare as ts
import yfinance as yf

import datetime
import pandas as pd

default_data_api = "tushare"
tushare_token = "88496aa09c93288465c2695e8ebf44f51442e0c7d3756d6485df3baa"

class pool:
    def __init__(self, market = "U.S.", method = "undefined", date = "today", max = 5000, dist = (-0.02,0.8,0.1)):
        self.market = market
        self.max = max
        self.dist = dist
        if method == "undefined":
            #default data api
            if market == "U.S.":
                self.method = "yfinance"
            elif market == "China-A":
                self.method = default_data_api
        if date == "today":
            self.date = datetime.datetime.now().strftime('%Y-%m-%d')
        else:
            self.date = date.strftime('%Y-%m-%d')

    def print_brief(self):
        print(self.market,self.method,self.date,self.max,self.dist)

    def get_df(self):
        pass
    
    def get_ticker(self):
        pass

    def assign_objective(self):
        pass


pool = pool()
pool.print_brief()
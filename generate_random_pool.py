import tushare as ts
import yfinance as yf
import random
import datetime
import pandas as pd
import numpy as np

default_data_api = "tushare"
tushare_token = "88496aa09c93288465c2695e8ebf44f51442e0c7d3756d6485df3baa"

class pool:
    def __init__(self, range = 256, market = "U.S.", method = "undefined", date = "today", max = 5000, dist = (-0.1,0.8,0.1)):
        self.range = range
        # update so that filter out stocks outside of date range later
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

        self.pool_list = self.get_ticker()
        self.objective_list = self.assign_objective()
        self.result = pd.DataFrame(list(zip(self.pool_list, self.objective_list)),
               columns =['stock_id', 'objective'])

    def print_brief(self):
        print(self.market,self.method,self.date,self.max,self.dist,len(self.pool_list))

    def get_df(self):
        return self.result
    
    def get_ticker(self):
        potential_list = pd.read_csv("sample_tickers.csv")["ticker"].to_list()
        # add only al those that are over days
        if self.max > len(potential_list):
            return random.sample(potential_list, len(potential_list))
        else:
            return random.sample(potential_list, self.max)

    def assign_objective(self):
        leng = len(self.pool_list)
            # Calculate standard deviation from variance
        std_dev = self.dist[2]

        # Generate normally distributed numbers
        samples = np.random.normal(loc=((self.dist[0] + self.dist[1]) / 2)-0.25, scale=std_dev, size=leng)

        # Clip values to stay within the bounds
        samples = np.clip(samples, self.dist[0], self.dist[1])

        return samples



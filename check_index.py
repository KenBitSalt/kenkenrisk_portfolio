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
            etf = yf.Ticker(self.ticker)
            # Get the top holdings (this may vary depending on data availability)
            holdings = etf.get_analysis()['holdings']
            # Check if holdings data is available
            if holdings is not None:
                # Create a DataFrame
                df_holdings = pd.DataFrame(holdings)
                # Calculate the weight of each holding
                df_holdings['Weight'] = df_holdings['Market Cap'] / df_holdings['Market Cap'].sum()
                # Display the holdings with calculated weights
                print(df_holdings[['Symbol', 'Market Cap', 'Weight']])
            else:
                print("Holdings data not available for this ticker.")

index_1 = index("SPY","U.S.")
index_1.get_weight()
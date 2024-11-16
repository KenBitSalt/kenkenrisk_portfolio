from polygon import RESTClient
import pandas as pd
client = RESTClient("")

import pandas_market_calendars as mcal
import datetime


today = datetime.datetime.now().strftime('%Y-%m-%d')
# Get the calendar for the New York Stock Exchange (NYSE)
nyse = mcal.get_calendar('NYSE')
late = nyse.schedule(start_date='2024-11-01', end_date=today)
latest_trade_day = mcal.date_range(late, frequency='1D')[-2].strftime('%Y-%m-%d')


result = pd.DataFrame(client.get_grouped_daily_aggs(date = latest_trade_day))
result.to_csv("sample_tickers.csv")
### returns a df of ticker, end_date, and certain length.

import yfinance as yf
import tushare as ts
import datetime
import pandas_market_calendars as mcal


def get_daily(ticker,end="today",length=365):
    if end == "today":
        today = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        today = "2025-06-19"
    start = (datetime.datetime.now() - datetime.timedelta(days=length)).strftime('%Y-%m-%d')

    # Get the calendar for the New York Stock Exchange (NYSE)
    nyse = mcal.get_calendar('NYSE')
    latest_trade_days = nyse.schedule(start_date='2024-11-01', end_date=today)

    # The previous market date ([-2]) ensures existence of data
    latest_trade_day = mcal.date_range(latest_trade_days, frequency='1D')[-2].strftime('%Y-%m-%d')
    stock = yf.Ticker(ticker)

    # GET TODAYS DATE AND CONVERT IT TO A STRING WITH YYYY-MM-DD FORMAT (YFINANCE EXPECTS THAT FORMAT)
    stock_hist = stock.history(start=start,end=latest_trade_day)
    stock_hist = stock_hist.reset_index(drop = False)
    #stock_hist['Date'] = stock_hist['Date'].astype(str)
    return stock_hist
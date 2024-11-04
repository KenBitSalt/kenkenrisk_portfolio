import yfinance as yf
import datetime


def get_daily(ticker,length=256):
    stock = yf.Ticker(ticker)
    # GET TODAYS DATE AND CONVERT IT TO A STRING WITH YYYY-MM-DD FORMAT (YFINANCE EXPECTS THAT FORMAT)
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_date = datetime.datetime.now() - datetime.timedelta(days=length)
    start_date = start_date.strftime('%Y-%m-%d')
    stock_hist = stock.history(start=start_date,end=end_date)
    stock_hist = stock_hist.reset_index(drop = False)
    return stock_hist
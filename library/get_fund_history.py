from pprint import pprint
import yfinance as yf
import pandas as pd
import os

FILE_DIR = '/Users/aripiralasrinivas/Data_Science/repos/mutual_funds_forecasting/input'
file_name = 'mutual_funds.csv'
file_path = os.path.join(FILE_DIR, file_name)
fund_df = pd.read_csv(file_path)

print(fund_df)
tickers = list(fund_df.Fund_Symbol.values)
tickers = [str(elem) for elem in tickers]
ticker_len = 1000
for i in range(0, len(tickers), ticker_len):
    tickers_1000 = tickers[i:(i+ticker_len)]

    print(tickers)
    tickers_str = " ".join(tickers_1000)
    file_appendix = f'_{i}-{i+ticker_len}'
    # print(tickers_str[:10])
    # tickers_str = "SPY AAPL MSFT"
  
    data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = tickers_str,
        # start="2020-10-22", end="2021-10-22",
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "1y",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1wk",

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        # group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = True,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )

    data['Close'].to_csv(os.path.join(FILE_DIR, f'mutual_funds_history-{file_appendix}.csv'), header=True)


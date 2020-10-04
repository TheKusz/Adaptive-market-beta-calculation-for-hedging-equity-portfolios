import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as pdr
import pickle
import requests
import yfinance as yf

yf.pdr_override()


class DataReader:
    def __init__(self):
        self.get_data_from_yahoo(self, True)
        self.compile_data(self)

    @staticmethod
    def save_sp500_tickers(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text.replace('.', '-')
            ticker = ticker[:-1]
            tickers.append(ticker)
        with open("sp500tickers.pickle", "wb") as f:
            pickle.dump(tickers, f)
        return tickers

    @staticmethod
    def get_data_from_yahoo(self, reload_sp500=False):
        if reload_sp500:
            tickers = self.save_sp500_tickers(self)
        else:
            with open("sp500tickers.pickle", "rb") as f:
                tickers = pickle.load(f)
        if not os.path.exists('stock_dfs'):
            os.makedirs('stock_dfs')

        start = dt.datetime(2000, 1, 1)
        end = dt.datetime.now()
        for ticker in tickers:
            print(ticker)
            if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
                df = pdr.get_data_yahoo(ticker, start, end)
                df.reset_index(inplace=True)
                df.set_index("Date", inplace=True)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            else:
                print('Already have {}'.format(ticker))

    @staticmethod
    def compile_data(self):
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

        main_open_df = pd.DataFrame()
        main_close_df = pd.DataFrame()
        main_daily_return_df = pd.DataFrame()

        for count, ticker in enumerate(tickers):
            open_df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            close_df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            daily_return_df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))

            open_df.set_index('Date', inplace=True)
            close_df.set_index('Date', inplace=True)
            daily_return_df.set_index('Date', inplace=True)

            open_df.rename(columns={'Open': ticker}, inplace=True)
            open_df.drop(['High', 'Low', 'Close', 'Adj Close', 'Volume'], 1, inplace=True)

            close_df.rename(columns={'Close': ticker}, inplace=True)
            close_df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], 1, inplace=True)

            daily_return_df['Daily Return'] = (daily_return_df['Close'] / daily_return_df['Open']) - 1
            daily_return_df.rename(columns={'Daily Return': ticker}, inplace=True)
            daily_return_df.drop(['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], 1, inplace=True)

            if main_open_df.empty:
                main_open_df = open_df
            else:
                main_open_df = main_open_df.join(open_df, how='outer')

            if main_close_df.empty:
                main_close_df = close_df
            else:
                main_close_df = main_close_df.join(close_df, how='outer')

            if main_daily_return_df.empty:
                main_daily_return_df = daily_return_df
            else:
                main_daily_return_df = main_daily_return_df.join(daily_return_df, how='outer')

            if count % 10 == 0:
                print(count)

        print(main_open_df.head())
        main_open_df.to_csv('sp500_joined_opens.csv')
        print(main_close_df.head())
        main_close_df.to_csv('sp500_joined_closes.csv')
        print(main_daily_return_df.head())
        main_daily_return_df.to_csv('sp500_joined_daily_returns.csv')

from DataLoader import DataReader
import pandas as pd
import pandas_datareader.data as pdr

dr = DataReader()
Cov = pd.DataFrame()

market_variance = dr.daily_return_df['Spy'].var()

beta = []
cov_vals = []
non_linear = 20
for beta_window in range(20, 5500, non_linear):
    narrowed = dr.daily_return_df.head(beta_window)
    covariance = pd.Series({symbol: dr.daily_return_df['SPY'].cov(dr.daily_return_df[symbol])
                     for symbol in dr.tickers
                     if symbol != 'SPY'})
    beta.append(covariance/market_variance)
    cov_vals.append(covariance)
    non_linear *= 20

print(cov_vals)
print(beta)

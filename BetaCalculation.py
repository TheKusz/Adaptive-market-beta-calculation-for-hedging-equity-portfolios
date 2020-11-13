from DataLoader import DataReader
import pandas as pd
import pandas_datareader.data as pdr

dr = DataReader()

non_linear = 20
# 5, 10, 20, 40, 60

for beta_window in [5, 10, 20, 40, 60]:
    covariance = pd.Series({symbol: dr.daily_return_df['SPY'].rolling(beta_window).cov(dr.daily_return_df[symbol])
                            for symbol in dr.tickers
                            if symbol != 'SPY'})
    market_variance = dr.daily_return_df['SPY'].rolling(beta_window).var()
    beta = covariance / market_variance

# beta * dr.daily_return_df['SPY']: piaci hozam rész
# hedged return: piactól független mozgásrésze
beta_err = beta * dr.daily_return_df['SPY'] - dr.daily_return_df

# cél: szórás csökkentése (beta err)
# nagy ugrásokra nem szabad számítani, azokat el kell dobni, ha rossz az érték
# más oldalakon is nagy az eltérés?
# notebook-ban inkább (in progress, végső)
# időben hogy alakul a hiba
# expanding: elejétől (ezzel is lehet)

# ? lehet-e tovább csökkenteni piactól függően a bétaerrort (nem csak fix értékként)



import yfinance as yf
import pandas as pd

class Portfolio:
    def __init__(self, config):
        self.config = config  # Diccionario con {ticker: número de acciones}

    @staticmethod
    def get_prices(ticker, timeframe, period):
        return yf.Ticker(ticker).history(period=period, interval=timeframe)['Close']

    def get_data(self, timeframe, period):
        hists = []
        for ticker, n_stocks in self.config.items():
            hists.append(self.get_prices(ticker, timeframe, period) * n_stocks)

        if hists:
            total_portfolio = pd.concat(hists, axis=1).sum(axis=1)
            return total_portfolio
        return None


if __name__ == '__main__':
    from config import portfolio_config
    print(Portfolio(portfolio_config).get_data(timeframe='1h',period='5d'))






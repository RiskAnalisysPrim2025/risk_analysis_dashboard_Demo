import yfinance as yf

class Portfolio:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def get_prices(ticker,timeframe,period):
        return yf.Ticker(ticker).history(period=period, interval=timeframe)['Close']

    def get_data(self, timeframe, periodo):
        hists = []
        for ticker,n_stocks in self.config.items():
            hists+=[self.get_prices(ticker,timeframe,periodo)*n_stocks]

        #TODO: sum historics and return them




if __name__ == '__main__':
    print(Portfolio.get_prices('AAPL', '1H', '5d'))



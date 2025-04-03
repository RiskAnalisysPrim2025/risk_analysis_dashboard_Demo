import numpy as np
from src.models.abstract_model import AbstractModel
from src.portfolio import Portfolio


class MAModel(AbstractModel):
    def __init__(self,portfolio:Portfolio,**kwargs):
        self.portfolio = portfolio
        self.window= kwargs['window']

    def get_variances(self, timeframe: str, period: str, future_periods:int)->list[float]:
        df = self.portfolio.get_data(timeframe, period)
        log_returns = np.log(df / df.shift(1))
        squared_returns = np.square(log_returns.iloc[-self.window:])
        variance = squared_returns.mean()
        return [variance]*future_periods


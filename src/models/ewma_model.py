from src.models.abstract_model import AbstractModel
from src.portfolio import Portfolio
import numpy as np

class EWMAModel(AbstractModel):
    def __init__(self,portfolio:Portfolio,**kwargs):
        self.portfolio = portfolio
        self.l=kwargs['lambda']

    def get_variances(self, timeframe: str, period: str, future_periods:int)->list[float]:
        df = self.portfolio.get_data(timeframe, period)
        log_returns = np.log(df / df.shift(1))

        r_squared= log_returns.iloc[-1:]**2
        sigma_squared = log_returns.var()

        ewma = (1-self.l) * r_squared + self.l * sigma_squared
        ewma=ewma.values[0]
        return [ewma]*future_periods




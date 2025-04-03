from src.models.abstract_model import AbstractModel
from src.portfolio import Portfolio


class GARCHModel(AbstractModel):
    def __init__(self,portfolio:Portfolio,**kwargs):
        self.portfolio = portfolio

    def get_variances(self, timeframe: str, period: str, future_periods:int)->list[float]:
        ...

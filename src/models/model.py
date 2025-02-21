from src.models.abstract_model import AbstractModel
from src.portfolio import Portfolio


class Model(AbstractModel):
    def __init__(self,portfolio:Portfolio):
        self.portfolio = portfolio

    def get_variance(self, timeframe: str, period: str):
        return self.portfolio.get_data(timeframe, period).pct_change().std() ** 2


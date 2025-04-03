from abc import ABC, abstractmethod
from src.portfolio import Portfolio


class AbstractModel(ABC):
    @abstractmethod
    def __init__(self, portfolio:Portfolio, **kwargs):
        pass

    @abstractmethod
    def get_variances(self, timeframe:str, period:str, future_periods:int)->list[float]:
        pass
from abc import ABC, abstractmethod
from src.portfolio import Portfolio


class AbstractModel(ABC):
    @abstractmethod
    def __init__(self, portfolio:Portfolio):
        pass

    @abstractmethod
    def get_variance(self, timeframe:str, period:str ):
        pass
from abc import ABC, abstractmethod
import pandas as pd


class DataframeCache(ABC):
    @abstractmethod
    def add_data(self, data: pd.DataFrame) -> str:
        pass

    @abstractmethod
    def get_data(self, key: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def remove_data(self, key: str) -> None:
        pass

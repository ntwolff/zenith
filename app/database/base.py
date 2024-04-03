from abc import ABC, abstractmethod

class BaseDatabase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def execute_query(self, query, **kwargs):
        pass

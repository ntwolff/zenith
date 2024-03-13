from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def execute_query(self, query, **kwargs):
        pass

    @abstractmethod
    def execute_query_async(self, query, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass
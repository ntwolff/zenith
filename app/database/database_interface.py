"""
Abstract database interfaces
"""

from abc import ABC, abstractmethod

class GraphDatabaseInterface(ABC):
    @abstractmethod
    def execute_query(self, query, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass

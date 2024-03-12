from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    def __init__(self, database):
        self.db = database

    @abstractmethod
    def process(self, event):
        pass
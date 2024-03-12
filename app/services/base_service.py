from abc import ABC

class BaseService(ABC):
    def __init__(self, database):
        self.db = database
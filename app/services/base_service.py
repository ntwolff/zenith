from abc import ABC
from app.database.database_interface import DatabaseInterface

class BaseService(ABC):
    def __init__(self, database: DatabaseInterface):
        self.db = database
from app.database.manager import DatabaseManager

class GraphRepository:
    def __init__(self, manager: DatabaseManager):
        self.db = manager.neo4j
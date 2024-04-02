"""
Neo4j graph database
"""

from neo4j import GraphDatabase
from app.database.database_interface import GraphDatabaseInterface
from app.config.settings import settings

class Neo4jDatabase(GraphDatabaseInterface):
    def __init__(self, uri=None, user=None, password=None):
        self.driver = GraphDatabase.driver(
            uri or settings.neo4j_uri,
            auth=(user or settings.neo4j_user, password or settings.neo4j_password)
        )

    def execute_query(self, query, **kwargs):
        with self.driver.session() as session:
            return session.run(query, **kwargs)

    def close(self):
        self.driver.close()

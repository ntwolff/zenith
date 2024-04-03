from neo4j import GraphDatabase
from app.database.base import BaseDatabase

class Neo4jDatabase(BaseDatabase):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def connect(self):
        return self.driver.session()

    def execute_query(self, query, **kwargs):
        with self.driver.session() as session:
            return session.run(query, **kwargs)

    def close(self):
        self.driver.close()

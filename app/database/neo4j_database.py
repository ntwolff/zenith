from neo4j import GraphDatabase
from app.config.settings import Settings

class Neo4jDatabase:
    def __init__(self):
        self.driver = GraphDatabase.driver(uri=Settings.neo4j_uri, auth=(Settings.neo4j_user, Settings.neo4j_password))

    def execute_query(self, query, **kwargs):
        with self.driver.session() as session:
            return session.run(query, **kwargs)

    def close(self):
        self.driver.close()
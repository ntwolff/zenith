import os

class Settings:
    neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://neo4j:7687')
    neo4j_user = os.environ.get('NEO4J_USERNAME', 'neo4j')
    neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')
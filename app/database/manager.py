from app.database.neo4j import Neo4jDatabase
from app.database.redis import RedisClient
from app.database.mongodb import MongoDBClient

class DatabaseManager:
    def __init__(self, settings):
        self.neo4j = Neo4jDatabase(settings.neo4j.neo4j_uri, settings.neo4j.neo4j_user, settings.neo4j.neo4j_password)
        
        #@TODO: Implement Redis and MongoDB
        #self.redis = RedisClient(settings.redis.redis_host, settings.redis.redis_port, settings.redis.redis_db, settings.redis.redis_password)
        #self.mongodb = MongoDBClient(settings.mongodb.mongodb_uri, settings.mongodb.mongodb_database)
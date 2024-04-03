from pymongo import MongoClient
from app.config.settings import settings

MongoDBClient = MongoClient(host=settings.mongodb.mongodb_uri).get_database(settings.mongodb.mongodb_database)
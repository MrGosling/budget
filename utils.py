from pymongo import MongoClient
from constants import MONGO_URI, DB_NAME, COLLECTION_NAME


def get_mongo_collection():
    """
    Возвращает коллекцию MongoDB, подключаясь по MONGO_URI.

    Возвращает:
        pymongo.collection.Collection: коллекция MongoDB
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

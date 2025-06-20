import os

from utils import load_environ

load_environ()

DB_NAME = os.getenv(key='DB_NAME')
MONGO_URI = os.getenv(key='MONGO_URI')
COLLECTION_NAME = os.getenv(key='COLLECTION_NAME')


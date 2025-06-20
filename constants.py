import os
from env_loader import load_environ

load_environ()

DB_NAME = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

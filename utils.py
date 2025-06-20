import os
from pathlib import Path

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


def load_environ() -> None:
    """
    Загружает переменные окружения из файла .env в текущей директории.

    Файл должен содержать строки в формате KEY=VALUE.
    Каждая переменная будет добавлена в os.environ.

    Исключения:
        Если файл .env не найден, выводится сообщение 'File not found!'.
    """
    try:
        env_path = Path('.') / '.env'
        with open(env_path) as file:
            for line in file:
                key, value = line.strip().split('=')
                os.environ[key] = value
    except FileNotFoundError:
        print('File not found!')

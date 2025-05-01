import os

from utils import load_environ

load_environ()

DB_PATH = os.getenv(key='DB_PATH')
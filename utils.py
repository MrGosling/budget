import os
from pathlib import Path
import sqlite3
from contextlib import contextmanager


@contextmanager
def conn_sqlite(db_path: str):
    """
    Здесь должен быть докстринг, описывающий функцию.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def load_environ() -> None:
    """
    Здесь должен быть докстринг, описывающий функцию.
    """
    try:
        env_path = Path('.') / '.env'
        with open(env_path) as file:
            for line in file:
                key, value = line.strip().split('=')
                os.environ[key] = value
    except FileNotFoundError:
        print('File not found!')

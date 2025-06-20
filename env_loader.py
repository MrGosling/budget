import os
from pathlib import Path

def load_environ() -> None:
    try:
        env_path = Path('.') / '.env'
        with open(env_path) as file:
            for line in file:
                key, value = line.strip().split('=')
                os.environ[key] = value
    except FileNotFoundError:
        print('File not found!')
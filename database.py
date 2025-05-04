import os

from constants import DB_PATH
from utils import conn_sqlite


def populate_table_with_fixtures(db_path):
    """
    Здесь должен быть докстринг, описывающий функцию.
    """
    fixtures = [
        {'expense': 'Оплата аренды', 'category': 'Жилье', 'amount': 15000.00, 'date': '01.01'},
        {'expense': 'Покупка продуктов', 'category': 'Еда', 'amount': 5000.00, 'date': '05.01'},
        {'expense': 'Оплата коммунальных услуг', 'category': 'Жилье', 'amount': 3000.00, 'date': '15.01'},

        {'expense': 'Покупка одежды', 'category': 'Одежда', 'amount': 2000.00, 'date': '01.02'},
        {'expense': 'Оплата интернета', 'category': 'Связь', 'amount': 1000.00, 'date': '10.02'},
        {'expense': 'Поездка на отдых', 'category': 'Развлечения', 'amount': 10000.00, 'date': '20.02'},

        {'expense': 'Покупка книг', 'category': 'Образование', 'amount': 1500.00, 'date': '01.03'},
        {'expense': 'Оплата телефона', 'category': 'Связь', 'amount': 1500.00, 'date': '05.03'},
        {'expense': 'Покупка подарков', 'category': 'Подарки', 'amount': 3000.00, 'date': '15.03'},

        {'expense': 'Покупка спортивных товаров', 'category': 'Спорт', 'amount': 2500.00, 'date': '01.04'},
        {'expense': 'Оплата страховки', 'category': 'Страхование', 'amount': 2000.00, 'date': '10.04'},
        {'expense': 'Поездка на природу', 'category': 'Развлечения', 'amount': 8000.00, 'date': '20.04'},
    ]

    with conn_sqlite(db_path) as conn:
        cursor = conn.cursor()
        for fixture in fixtures:
            cursor.execute('''
                INSERT INTO budget (expense, category, amount, date)
                VALUES (?, ?, ?, ?)
            ''', (fixture['expense'], fixture['category'], fixture['amount'], fixture['date']))
        conn.commit()
    print('Таблица успешно наполнена фикстурными данными!')


def create_db_and_table(db_path: str, overwrite: bool = False):
    """
    Здесь должен быть докстринг, описывающий функцию.
    """
    exists = os.path.exists(db_path)
    if not exists or overwrite:
        if not exists:
            print(f'Файл базы данных {db_path} не существует. Создаем...')
        elif overwrite:
            print(f'Файл базы данных {db_path} уже существует. Перезаписываю...')
        with conn_sqlite(db_path) as conn:
            cursor = conn.cursor()
            if exists and overwrite:
                cursor.execute('DROP TABLE budget;')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budget (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expense TEXT,
                    category TEXT,
                    amount REAL,
                    date DATE
                    )
            ''')
            
            conn.commit()
            populate_table_with_fixtures(db_path)
            
            print(f'База данных и таблица "{db_path}" успешно созданы!')
    else:
        print(f'Файл базы данных {db_path} уже существует.')


def main():
    create_db_and_table()

if __name__ == "__main__":
    main()

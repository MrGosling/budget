from constants import DB_PATH
from utils import conn_sqlite

class Budget:
    def __init__(self, db_path=DB_PATH):
        """
        Здесь должен быть докстринг.
        """
        self.db_path = db_path

    def add_expense(self, expense, category, amount, date):
        """
        Добавляет новую трату в базу данных.
        
        Параметры:
            expense (str): Наименование траты
            category (str): Категория траты
            amount (float): Сумма траты
            date (str): Дата траты в формате 'YYYY-MM-DD'
            
        Возвращает:
            None
        """
        with conn_sqlite(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            INSERT INTO expenses (expense, category, amount, date)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (expense, category, amount, date))
            conn.commit()

    def get_the_most_expensive_category(self, date):
        """
        Возвращает категорию с наибольшими тратами за указанную дату.
        
        Параметры:
            date (str): Дата в формате 'YYYY-MM-DD'
            
        Возвращает:
            dict: Словарь с ключами 'category' и 'total_amount', 
                  содержащий название категории и общую сумму трат в ней.
                  Если данных нет, возвращает None.
        """
        with conn_sqlite(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            SELECT category, SUM(amount) as total_amount
            FROM expenses
            WHERE date = ?
            GROUP BY category
            ORDER BY total_amount DESC
            LIMIT 1
            """
            cursor.execute(query, (date,))
            result = cursor.fetchone()
            return dict(result) if result else None


    def get_the_most_expensive_purchase(self, category, date):
        """
        Возвращает самую дорогую покупку в указанной категории за указанную дату.
        
        Параметры:
            category (str): Название категории
            date (str): Дата в формате 'YYYY-MM-DD'
            
        Возвращает:
            dict: Словарь с ключами 'expense', 'amount' и 'date',
                  содержащий информацию о покупке.
                  Если данных нет, возвращает None.
        """
        with conn_sqlite(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            SELECT expense, amount, date
            FROM expenses
            WHERE category = ? AND date = ?
            ORDER BY amount DESC
            LIMIT 1
            """
            cursor.execute(query, (category, date))
            result = cursor.fetchone()
            return dict(result) if result else None

if __name__ == "__main__":
    budget = Budget()
    budget.add_expense(1,1,1,1)

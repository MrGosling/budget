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
            date (str): Дата траты в формате 'day.month'
            
        Возвращает:
            successsCode (bin): код выполнения)
        """         

        maxDaysLengths = {0:31, 1:30, 2:29}

        successCode = 0
        
        dateTemp = date.split(sep='.')
        if len(dateTemp) == 2:
            day = dateTemp[0]
            month = dateTemp[1]
            if amount.isdigit():
                if day.isdigit() and month.isdigit() and int(month) in range(1, 13):
                    month = int(month)
                    day = int(day)
                    if day <= maxDaysLengths[(month % 2) + ((month / 2 == 1) * 2)]:
                        date = str(day).zfill(2) + '.' + str(month).zfill(2)
                        with conn_sqlite(self.db_path) as conn:
                            cursor = conn.cursor()
                            query = """
                            INSERT INTO database (expense, category, amount, date)
                            VALUES (?, ?, ?, ?)
                            """
                            cursor.execute(query, (expense, category, amount, date))
                            conn.commit()
                            successCode = 2
            else:
                successCode = 1

        return successCode

    def get_the_most_expensive_category(self, date):
        """
        Возвращает категорию с наибольшими тратами за указанную дату.
        
        Параметры:
            date (str): Дата в формате 'day.month'
            
        Возвращает:
            dict: Словарь с ключами 'category' и 'total_amount', 
                  содержащий название категории и общую сумму трат в ней.
                  Если данных нет, возвращает None.
        """
        with conn_sqlite(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            SELECT category, SUM(amount) as total_amount
            FROM database
            WHERE (substr(date,4,5)) = ?
            GROUP BY category
            ORDER BY total_amount DESC
            LIMIT 1
            """
            cursor.execute(query, (date,))
            result = cursor.fetchone()
            return dict(result) if result else None


    def get_the_most_expensive_purchase(self, category, month):
        """
        Возвращает самую дорогую покупку в указанной категории за указанную дату.
        
        Параметры:
            category (str): Название категории
            date (str): Дата в формате 'day.month'
            
        Возвращает:
            dict: Словарь с ключами 'expense', 'amount' и 'date',
                  содержащий информацию о покупке.
                  Если данных нет, возвращает None.
        """
        with conn_sqlite(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
            SELECT expense, amount, date
            FROM database
            WHERE category = ? AND (substr(date,4,5)) = ?
            ORDER BY amount DESC
            LIMIT 1
            """
            cursor.execute(query, (category, month))
            result = cursor.fetchone()
            return dict(result) if result else None

if __name__ == "__main__":
    budget = Budget()

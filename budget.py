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
        Здесь должен быть докстринг, описывающий добавление траты.
        """
        with conn_sqlite(self.db_path) as conn:
            pass

    def get_the_most_expensive_category(self, date):
        """
        Здесь должен быть докстринг, описывающий получение самой затратной категории.
        """
        with conn_sqlite(self.db_path) as conn:
            pass

    def get_the_most_expensive_purchase(self, category, date):
        """
        Здесь должен быть докстринг, описывающий получение самой дорогой покупки.
        """
        with conn_sqlite(self.db_path) as conn:
            pass

if __name__ == "__main__":
    budget = Budget()
# init my branch
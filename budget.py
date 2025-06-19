from utils import get_mongo_collection


class Budget:
    def __init__(self):
        """
        Класс для управления бюджетом с использованием MongoDB.
        """
        self.collection = get_mongo_collection()

    def add_expense(self, expense, category, amount, date):
        """
        Добавляет новую трату в базу данных.

        Параметры:
            expense (str): Наименование траты
            category (str): Категория траты
            amount (str/float): Сумма траты
            date (str): Дата траты в формате 'day.month'

        Возвращает:
            int: Код выполнения (0 = ошибка валидации, 1 = ошибка типа, 2 = успешно)
        """
        maxDaysLengths = {0: 31, 1: 30, 2: 29}
        successCode = 0

        date_parts = date.split('.')
        if len(date_parts) == 2:
            day, month = date_parts
            if str(amount).replace('.', '', 1).isdigit():
                if day.isdigit() and month.isdigit() and 1 <= int(month) <= 12:
                    month = int(month)
                    day = int(day)
                    if day <= maxDaysLengths[(month % 2) + ((month / 2 == 1) * 2)]:
                        formatted_date = str(day).zfill(2) + '.' + str(month).zfill(2)

                        self.collection.insert_one({
                            'expense': expense,
                            'category': category,
                            'amount': float(amount),
                            'date': formatted_date
                        })

                        successCode = 2
            else:
                successCode = 1

        return successCode

    def get_the_most_expensive_category(self, date):
        """
        Возвращает категорию с наибольшими тратами за указанный месяц.

        Параметры:
            date (str): Дата в формате 'day.month' или просто 'month'

        Возвращает:
            dict | None: {'category': str, 'total_amount': float} или None
        """
        month = date.split('.')[1] if '.' in date else date
        pipeline = [
            {"$match": {"date": {"$regex": f"\\.{str(month).zfill(2)}$"}}},
            {"$group": {"_id": "$category", "total_amount": {"$sum": "$amount"}}},
            {"$sort": {"total_amount": -1}},
            {"$limit": 1}
        ]

        result = list(self.collection.aggregate(pipeline))
        if result:
            return {'category': result[0]['_id'], 'total_amount': result[0]['total_amount']}
        return None

    def get_the_most_expensive_purchase(self, category, month):
        """
        Возвращает самую дорогую покупку в указанной категории за указанный месяц.

        Параметры:
            category (str): Название категории
            month (str): Месяц в формате 'MM' или дата 'DD.MM'

        Возвращает:
            dict | None: {'expense': str, 'amount': float, 'date': str} или None
        """
        month = month.split('.')[1] if '.' in month else month
        query = {
            "category": category,
            "date": {"$regex": f"\\.{str(month).zfill(2)}$"}
        }

        result = self.collection.find(query).sort("amount", -1).limit(1)
        doc = next(result, None)
        if doc:
            return {
                "expense": doc["expense"],
                "amount": doc["amount"],
                "date": doc["date"]
            }
        return None


if __name__ == "__main__":
    budget = Budget()
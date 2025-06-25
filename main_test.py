import pytest
from pymongo import MongoClient
from budget import Budget
from database import (
    get_mongo_collection,
    populate_collection_with_fixtures,
    create_db_and_collection,
    fixtures
)


# Фикстуры для тестовой базы данных
@pytest.fixture(scope="module")
def test_db():
    """Фикстура для тестовой базы MongoDB."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_budget_db"]
    yield db
    client.drop_database("test_budget_db")


@pytest.fixture
def clean_collection(test_db):
    """Очищает коллекцию перед каждым тестом."""
    collection = test_db["expenses"]
    collection.delete_many({})
    return collection


@pytest.fixture
def budget(test_db):
    """Фикстура для класса Budget с тестовой коллекцией."""
    budget = Budget()
    budget.collection = test_db["expenses"]
    return budget


# Вспомогательные функции
def add_test_data(collection, data):
    """Добавляет тестовые данные в коллекцию."""
    collection.insert_many(data)


# Тесты для database.py
def test_get_mongo_collection():
    """Проверяет, что подключение к MongoDB работает."""
    collection = get_mongo_collection()
    assert collection.name == "expenses"
    assert collection.database.name == "budget_db"


# Тесты для budget.py
class TestBudgetOperations:
    """Группа тестов для операций с бюджетом."""
    
    @pytest.fixture(autouse=True)
    def setup(self, budget, clean_collection):
        self.budget = budget
        self.collection = budget.collection


    def test_add_expense_success(self):
        """Проверка успешного добавления траты."""
        result = self.budget.add_expense("Кофе", "Еда", "150.50", "10.05")
        assert result == 2
        
        expense = self.collection.find_one({"expense": "Кофе"})
        assert expense["category"] == "Еда"
        assert expense["amount"] == 150.50
        assert expense["date"] == "10.05"


    def test_add_expense_invalid_date(self):
        """Проверка невалидной даты."""
        assert self.budget.add_expense("Телефон", "Техника", "50000", "32.01") == 0


    def test_add_expense_invalid_amount(self):
        """Проверка невалидной суммы."""
        assert self.budget.add_expense("Книга", "Образование", "десять рублей", "15.06") == 1


    def test_get_the_most_expensive_category(self):
        """Проверка самой затратной категории."""
        add_test_data(self.collection, [
            {"expense": "Кофе", "category": "Еда", "amount": 150.50, "date": "10.05"},
            {"expense": "Обед", "category": "Еда", "amount": 500, "date": "12.05"},
            {"expense": "Бензин", "category": "Транспорт", "amount": 2000, "date": "15.05"},
        ])
        result = self.budget.get_the_most_expensive_category("05")
        assert result == {"category": "Транспорт", "total_amount": 2000}


    def test_get_the_most_expensive_purchase(self):
        """Проверка самой дорогой покупки."""
        add_test_data(self.collection, [
            {"expense": "Кофе", "category": "Еда", "amount": 150, "date": "10.05"},
            {"expense": "Рестоан", "category": "Еда", "amount": 3000, "date": "12.05"},
            {"expense": "Супермаркет", "category": "Еда", "amount": 2000, "date": "15.05"},
        ])
        result = self.budget.get_the_most_expensive_purchase("Еда", "05")
        assert result["expense"] == "Рестоан"
        assert result["amount"] == 3000


    def test_get_no_data_cases(self):
        """Проверка случаев с отсутствием данных."""
        assert self.budget.get_the_most_expensive_category("12") is None
        assert self.budget.get_the_most_expensive_purchase("Развлечения", "01") is None


def test_fixtures_data():
    """Тест структуры тестовых данных."""
    assert len(fixtures) == 12
    for item in fixtures:
        assert set(item.keys()) == {'expense', 'category', 'amount', 'date'}
        assert isinstance(item['expense'], str)
        assert isinstance(item['category'], str)
        assert isinstance(item['amount'], float)
        assert isinstance(item['date'], str)


def test_populate_collection_with_fixtures(clean_collection, monkeypatch):
    """Тест заполнения коллекции фикстурами."""
    # Мокаем get_mongo_collection чтобы возвращать тестовую коллекцию
    monkeypatch.setattr('database.get_mongo_collection', lambda: clean_collection)
    
    # Проверяем пустую коллекцию
    assert clean_collection.count_documents({}) == 0
    
    populate_collection_with_fixtures()
    
    # Проверяем что данные добавились
    assert clean_collection.count_documents({}) == 12
    
    # Проверяем первый документ
    first_item = clean_collection.find_one({})
    assert first_item['expense'] == 'Оплата аренды'
    assert first_item['category'] == 'Жилье'
    assert first_item['amount'] == 15000.0
    assert first_item['date'] == '01.01'


def test_create_db_and_collection_create_new(clean_collection, monkeypatch):
    """Тест команды create для новой коллекции."""
    # Мокаем get_mongo_collection чтобы возвращать тестовую коллекцию
    monkeypatch.setattr('database.get_mongo_collection', lambda: clean_collection)
    
    assert clean_collection.count_documents({}) == 0
    create_db_and_collection('create')
    assert clean_collection.count_documents({}) == 12


def test_create_db_and_collection_rewrite(clean_collection, monkeypatch):
    """Тест команды rewrite."""
    # Мокаем get_mongo_collection чтобы возвращать тестовую коллекцию
    monkeypatch.setattr('database.get_mongo_collection', lambda: clean_collection)
    
    # Добавляем тестовые данные
    clean_collection.insert_many([{'test': 'data1'}, {'test': 'data2'}])
    assert clean_collection.count_documents({}) == 2
    
    create_db_and_collection('rewrite')
    # Должны получить фикстуры
    assert clean_collection.count_documents({}) == 12


def test_create_db_and_collection_delete(clean_collection, monkeypatch):
    """Тест команды delete."""
    # Мокаем get_mongo_collection чтобы возвращать тестовую коллекцию
    monkeypatch.setattr('database.get_mongo_collection', lambda: clean_collection)
    
    # Добавляем тестовые данные
    clean_collection.insert_many([{'test': 'data1'}, {'test': 'data2'}])
    assert clean_collection.count_documents({}) == 2
    
    create_db_and_collection('delete')
    assert clean_collection.count_documents({}) == 0


def test_create_db_and_collection_invalid_command(clean_collection, monkeypatch, capsys):
    """Тест обработки неверной команды."""
    # Мокаем get_mongo_collection чтобы возвращать тестовую коллекцию
    monkeypatch.setattr('database.get_mongo_collection', lambda: clean_collection)
    
    create_db_and_collection('invalid_command')
    captured = capsys.readouterr()
    assert "Неизвестная команда" in captured.out


def test_main_function(clean_collection, monkeypatch):
    """Тест main функции."""
    # Мокаем input чтобы возвращал 'create'
    monkeypatch.setattr('builtins.input', lambda _: 'create')
    # Мокаем get_mongo_collection чтобы возвращать тестовую коллекцию
    monkeypatch.setattr('database.get_mongo_collection', lambda: clean_collection)
    
    from database import main
    main()
    
    assert clean_collection.count_documents({}) == 12


if __name__ == "__main__":
    pytest.main(["-v"])
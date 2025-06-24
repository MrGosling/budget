from utils import get_mongo_collection

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


def populate_collection_with_fixtures():
    """
    Наполнение MongoDB фикстурами.
    """
    collection = get_mongo_collection()
    collection.insert_many(fixtures)
    print('Коллекция успешно наполнена фикстурными данными!')


def create_db_and_collection(command: str):
    """
    Взаимодействие с MongoDB в зависимости от команды:
    - 'create': создание коллекции и наполнение фикстурами, если её нет;
    - 'rewrite': очистка и перезаполнение коллекции;
    - 'delete': удаление коллекции.
    """
    collection = get_mongo_collection()

    if command == 'create':
        if collection.estimated_document_count() == 0:
            populate_collection_with_fixtures()
            print('Коллекция создана и заполнена.')
        else:
            print("Коллекция уже существует. Используйте 'rewrite' для перезаписи.")
    elif command == 'rewrite':
        collection.drop()
        print('Коллекция удалена.')
        populate_collection_with_fixtures()
    elif command == 'delete':
        collection.drop()
        print('Коллекция удалена.')
    else:
        print("Неизвестная команда. Используйте 'create', 'rewrite' или 'delete'.")


def main():
    # Например, можно изменить на 'create', 'rewrite' или 'delete'
    create_db_and_collection('create')


if __name__ == '__main__':
    main()

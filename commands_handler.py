import os
from budget import Budget
import database
from constants import DB_NAME
from utils import get_mongo_collection


def commands_handler(input_data):
    temp = ''
    argsList = []
    string_closed = True

    for symbol_id in range(len(input_data)):
        symbol = input_data[symbol_id]
        if symbol in ('"', "'"):
            string_closed = not string_closed
        elif symbol == ' ' and string_closed:
            argsList.append(temp)
            temp = ''
        else:
            temp += symbol

    if temp != '':
        argsList.append(temp)

    lenArgsList = len(argsList)

    def printHelp():
        print('Commands handler usage:\n'
              '\t"help" - вывести это сообщение\n'
              '\t"add" - Добавить трату\n'
              '\t"most_expensive_category" - Самая затратная категория\n'
              '\t"most_expensive_purchase" - Самая дорогая покупка за месяц + категория\n'
              '\t"db" - действия с базой данных\n'
              '\t"cls" - очистить консоль\n'
              '\t"exit" - выйти из программы\n')

    def printWrongArgs(commandArgsCount: int):
        word = 'arguments' if commandArgsCount > 1 else 'argument'
        print(f'Wrong input: command takes {commandArgsCount} {word}\n'
              f'Instead {lenArgsList - 1} was given')

    budget = Budget()

    def db_exists():
        """Проверка существования коллекции (MongoDB не требует файла как SQLite)."""
        collection = get_mongo_collection()
        return collection.estimated_document_count() > 0

    if argsList[0] != '':
        match argsList[0]:
            case 'add':
                match lenArgsList:
                    case 1:
                        print('"add" command takes 4 arguments: '
                              'expense, category, amount, date')
                    case 5:
                        expense, category, amount, date = argsList[1:]
                        if db_exists():
                            successCode = budget.add_expense(expense, category, amount, date)
                            successMessages = {
                                0: 'Ошибка: неправильный тип даты. (должно быть "[день].[месяц]")',
                                1: 'Ошибка: неправильная цена. (должна быть числом)',
                                2: 'Трата добавлена успешно'
                            }
                            print(successMessages[successCode])
                        else:
                            print("База пуста. Выполните команду 'db create' или 'db rewrite'")
                    case _:
                        printWrongArgs(4)

            case 'most_expensive_category':
                match lenArgsList:
                    case 1:
                        print('"most_expensive_category" command takes 1 argument: month')
                    case 2:
                        month = argsList[1]
                        if month.isdigit() and 1 <= int(month) <= 12:
                            month = str(int(month)).zfill(2)
                            if db_exists():
                                result = budget.get_the_most_expensive_category(month)
                                if result is None:
                                    print('Ничего не найдено за этот месяц.')
                                else:
                                    print(f'Самая затратная категория за этот месяц: '
                                          f'"{result["category"]}" суммой в {result["total_amount"]} попугаев.')
                            else:
                                print("База пуста. Выполните команду 'db create' или 'db rewrite'")
                        else:
                            print('Некорректный аргумент: месяц должен быть от 1 до 12')
                    case _:
                        printWrongArgs(1)

            case 'most_expensive_purchase':
                match lenArgsList:
                    case 1:
                        print('"most_expensive_purchase" command takes 2 arguments: '
                              'category, month')
                    case 3:
                        category, month = argsList[1:]
                        if month.isdigit() and 1 <= int(month) <= 12:
                            month = str(int(month)).zfill(2)
                            if db_exists():
                                result = budget.get_the_most_expensive_purchase(category, month)
                                if result is None:
                                    print('Ничего не найдено за этот месяц.')
                                else:
                                    print(f'Самая дорогая покупка в категории {category} '
                                          f'за этот месяц: {result["expense"]} '
                                          f'ценой в {result["amount"]}, дата: {result["date"]}')
                            else:
                                print("База пуста. Выполните команду 'db create' или 'db rewrite'")
                        else:
                            print('Некорректный аргумент: месяц должен быть от 1 до 12')
                    case _:
                        printWrongArgs(2)

            case 'db':
                match lenArgsList:
                    case 1:
                        print('"db" command takes 1 argument: [create | delete | rewrite]')
                    case 2:
                        database.create_db_and_collection(argsList[1])
                    case _:
                        printWrongArgs(1)

            case 'help':
                printHelp()

            case 'cls':
                os.system('cls' if os.name == 'nt' else 'clear')

            case 'exit':
                print('Выход из программы...')
                exit()

            case _:
                print('Неизвестная команда. Введите "help" для справки.')
    else:
        printHelp()
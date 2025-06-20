import os
import database

from budget import Budget
from utils import get_mongo_collection


def commands_handler(input_data):
    temp = ''
    args_list = []
    string_closed = True

    for symbol_id in range(len(input_data)):
        symbol = input_data[symbol_id]
        if symbol in ('"', "'"):
            string_closed = not string_closed
        elif symbol == ' ' and string_closed:
            args_list.append(temp)
            temp = ''
        else:
            temp += symbol

    if temp != '':
        args_list.append(temp)


    len_args_list = len(args_list)


    def print_help():
        print('Commands handler usage:\n'
              '\t"help" - вывести это сообщение\n'
              '\t"add" - Добавить трату\n'
              '\t"most_expensive_category" - Самая затратная категория\n'
              '\t"most_expensive_purchase" - Самая дорогая покупка за месяц + категория\n'
              '\t"db" - действия с базой данных\n'
              '\t"cls" - очистить консоль\n'
              '\t"exit" - выйти из программы\n')


    def print_wrong_args(commandArgsCount: int):
        word = 'arguments' if commandArgsCount > 1 else 'argument'
        print(f'Wrong input: command takes {commandArgsCount} {word}\n'
              f'Instead {len_args_list - 1} was given')


    budget = Budget()


    def db_exists():
        """Проверка существования коллекции (MongoDB не требует файла как SQLite)."""
        collection = get_mongo_collection()
        return collection.estimated_document_count() > 0


    if args_list[0] != '':
        match args_list[0]:
            case 'add':
                match len_args_list:
                    case 1:
                        print('"add" command takes 4 arguments: '
                              'expense, category, amount, date')
                    case 5:
                        expense, category, amount, date = args_list[1:]
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
                        print_wrong_args(4)

            case 'most_expensive_category':
                match len_args_list:
                    case 1:
                        print('"most_expensive_category" command takes 1 argument: month')
                    case 2:
                        month = args_list[1]
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
                        print_wrong_args(1)

            case 'most_expensive_purchase':
                match len_args_list:
                    case 1:
                        print('"most_expensive_purchase" command takes 2 arguments: '
                              'category, month')
                    case 3:
                        category, month = args_list[1:]
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
                        print_wrong_args(2)

            case 'db':
                match len_args_list:
                    case 1:
                        print('"db" command takes 1 argument: [create | delete | rewrite]')
                    case 2:
                        database.create_db_and_collection(args_list[1])
                    case _:
                        print_wrong_args(1)

            case 'help':
                print_help()

            case 'cls':
                os.system('cls' if os.name == 'nt' else 'clear')

            case 'exit':
                print('Выход из программы...')
                exit()

            case _:
                print('Неизвестная команда. Введите "help" для справки.')
    else:
        print_help()
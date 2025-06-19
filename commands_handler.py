import os
from budget import Budget
import database
from constants import DB_PATH

#функция выводит справку о всех командах
def printHelp():
    print('Commands handler usage:\n'
        '\t"help" - вывести это сообщение\n'
        '\t"add" - Добавить трату\n'
        '\t"most_expensive_category" - Самая затратная категория\n'
        '\t"most_expensive_purchase" - Самая дорогая покупка за месяц + категория\n'
        '\t"db" - действия с базой данных\n'
        '\t"cls" - очистить консоль\n'
        '\t"exit" - выйти из программы\n'
        )

#печатает в консоль сообщение о том, что количество аргументов непрпавильно
#печатает количество аргументов, которые дал пользователь (commnadArgsCount)
def printWrongArgs(lenArgsList: int, commandArgsCount: int):
    if commandArgsCount > 1: str = 'arguments'
    else: str = 'argument'
    print(f'Wrong input: command takes {commandArgsCount} {str}\n'
        f'Instead {lenArgsList - 1} was given')

#главная штука функция
def commands_handler(input_data):

    temp = ''
    argsList = []

    string_closed = True

    #разделяет строку input_data на список строк по пробелу или кавычкам
    for symbol_id in range(len(input_data)):
        symbol = input_data[symbol_id]
        if symbol == '"' or symbol == "'":
            string_closed = not string_closed
        elif symbol == ' ' and string_closed:
            argsList.append(temp)
            temp = ''
        else:
            temp += symbol

    #если полученный из разделителя список не пуст, то добавляем его в argsList, а если нет, то argsList остается пустым
    if temp != '':
        argsList.append(temp)
    #запоминаем длину списка argsList   
    lenArgsList = len(argsList)

    budget = Budget()

    exists = os.path.exists(DB_PATH)

    no_db = lambda: print("Файл базы данных не найден.")

    #обработчик команд

    #если список аргументов не пустой
    if argsList[0] != '':
        #соотнесение первого аргумента
        match(argsList[0]):
            case('add'):
                match(lenArgsList):
                    case(1):
                        print('"add" command takes 4 arguments: '
                              'expense, category, amount, date')
                    case(5):
                        if exists:
                            expense, category, amount, date = argsList[1:]
                            successCode = budget.add_expense(expense, category, amount, date)
                            successCodes = {
                                0:'Ошибка: неправильный тип даты. (должно быть "[день].[месяц]")',
                                1:'Ошибка: неправильная цена. (должна быть числом)',
                                2:'Трата добавлена успешно'
                            }
                            print(successCodes[successCode])
                        else:
                            no_db()
                    case _:
                        printWrongArgs(lenArgsList, 4)
            case('most_expensive_category'):
                match(lenArgsList):
                    case(1):
                        print('"most_expensive_category" command takes 1 argument: '
                        'month')
                    case(2):
                        if exists:
                            month = argsList[1]
                            if month.isdigit() and int(month) > 0 and int(month) < 13:
                                month = str(int(month)).zfill(2)
                                result = budget.get_the_most_expensive_category(month)
                                if result == None:
                                    print('Ничего не найдено за этот месяц.')
                                else:
                                    print(f'Самая затратная категория за этот месяц: '
                                          f'"{result["category"]}" суммой в '
                                          f'{result["total_amount"]} попугаев.')
                            else:
                                print('Некорректный аргумент')
                        else:
                            no_db()
                    case _:
                        printWrongArgs(lenArgsList, 1)
            case('most_expensive_purchase'):
                match(lenArgsList):
                    case(1):
                        print('"most_expensive_purchase" command takes 2 arguments: '
                        'category, month')
                    case(3):
                        if exists:
                            category, month = argsList[1:]
                            if month.isdigit() and int(month) > 0 and int(month) < 13:
                                month = str(int(month)).zfill(2)
                                result = budget.get_the_most_expensive_purchase(category, month)
                                if result == None:
                                    print('Ничего не найдено за этот месяц.')
                                else:
                                    print(f'Самая дорогая покупка в категории {category} '
                                          f'за этот месяц: {result["expense"]} '
                                          f'ценой в {result["amount"]}, дата: {result["date"]}')
                            else:
                                print('Некорректный аргумент')
                        else:
                            no_db()
                    case _:
                        printWrongArgs(lenArgsList, 2)
            case('db'):
                match(lenArgsList):
                    case(1):
                        print('"db" command takes 1 argument: '
                              '[create | delete | rewrite]'
                              )
                    case(2):
                        database.create_db_and_table(argsList[1])
                    case _:
                        printWrongArgs(lenArgsList, 1)
            case('help'):
                printHelp()
            
            case _:
                print(f'Unkown command. Type "help" for help')

    else:
        printHelp()    

import sys
import os
from budget import Budget

def commands_handler():
    argsList = sys.argv
    argsList = ' '.join(argsList[2:]).split(' - ')
    lenArgsList = len(argsList)

    def printHelp():
        print('Usage:\n'
            'add - Добавить трату\n'
            'most_expensive_category - Самая затратная категория\n'
            'most_expensive_purchase - Самая дорогая покупка\n'
            'help - вывести этот список'
            )

    def printWrongArgs(commandArgsCount: int):
        if commandArgsCount > 1: str = 'arguments'
        else: str = 'argument'
        print(f'Wrong input: commands takes {commandArgsCount} {str}\n'
            f'Instead {lenArgsList - 1} was given')

    budget = Budget()

    if argsList[0] != '':
        match(argsList[0]):
            case('add'):
                match(lenArgsList):
                    case(1):
                        print('add command takes 4 arguments: '
                              'expense, category, amount, date')
                    case(5):
                        expense, category, amount, date = argsList[1:]
                        successCode = budget.add_expense(expense, category, amount, date)
                        successCodes = {
                            0:'Ошибка: неправильный тип даты. (должно быть "[день].[месяц]")',
                            1:'Ошибка: неправильная цена. (должна быть числом)',
                            2:'Трата добавлена успешно'
                        }
                        print(successCodes[successCode])
                    case _:
                        printWrongArgs(4)
            case('most_expensive_category'):
                match(lenArgsList):
                    case(1):
                        print('most_expensive_category command takes 1 argument: '
                        'date')
                    case(2):
                        date = argsList[1]
                        result = budget.get_the_most_expensive_category(date)
                        print(f'Самая затратная категория за {date}: {result}')
                    case _:
                        printWrongArgs(1)
            case('most_expensive_purchase'):
                match(lenArgsList):
                    case(1):
                        print('most_expensive_purchase command takes 1 argument: '
                        'category, date')
                    case(3):
                        category, date = argsList[1:]
                        result = budget.get_the_most_expensive_purchase(category, date)
                        print(f'Самая дорогая покупка в категории {category} за {date}: {result}')
                    case _:
                        printWrongArgs(2)
            case('help'):
                printHelp()
            case _:
                print(f'Unkown command. Type "{os.path.basename(__file__)} -help" for help')

    else:
        printHelp()    

commands_handler()

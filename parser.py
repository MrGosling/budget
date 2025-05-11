import argparse
from budget import Budget

def main():
    parser = argparse.ArgumentParser(description='Утилита для управления бюджетом')
    
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Добавить трату')
    add_parser.add_argument('-e', '--expense', required=True, help='Наименование траты')
    add_parser.add_argument('-c', '--category', required=True, help='Категория траты')
    add_parser.add_argument('-a', '--amount', required=True, help='Сумма траты')
    add_parser.add_argument('-d', '--date', required=True, help='Дата траты')

    category_parser = subparsers.add_parser('most_expensive_category', help='Самая затратная категория')
    category_parser.add_argument('-d', '--date', required=True, help='Дата для анализа')

    purchase_parser = subparsers.add_parser('most_expensive_purchase', help='Самая дорогая покупка')
    purchase_parser.add_argument('-c', '--category', required=True, help='Категория для анализа')
    purchase_parser.add_argument('-d', '--date', required=True, help='Дата для анализа')

    args = parser.parse_args()

    budget = Budget()

    if args.command == 'add':
        budget.add_expense(args.expense, args.category, args.amount, args.date)
        print('Трата добавлена успешно.')
    elif args.command == 'most_expensive_category':
        result = budget.get_the_most_expensive_category(args.date)
        print(f'Самая затратная категория за {args.date}: {result}')
    elif args.command == 'most_expensive_purchase':
        result = budget.get_the_most_expensive_purchase(args.category, args.date)
        print(f'Самая дорогая покупка в категории {args.category} за {args.date}: {result}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

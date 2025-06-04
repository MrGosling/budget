from fastapi import FastAPI, Response, status
import uvicorn
from pydantic import BaseModel

from budget import Budget

app = FastAPI()
budget = Budget()


@app.get('/')
async def read_root():
    """Рутовая заглушка"""
    return {'result': 'SUCCESS', 'text': 'Wellcome to the budget service!'}


@app.get('/healthcheck')
async def get_healthcheck():
    """Возвращает сообщение о статусе сервиса"""
    return {'result': 'SUCCESS', 'text': 'OK'}


# Возвращает список эндпоинтов сервиса
@app.get('/v1/help')
async def help_list():
    """Выводит список доступных команд."""
    return {
        'commands': [
            {'method': 'POST', 'path': '/v1/expenses', 'description': 'Добавить трату'},
            {'method': 'GET', 'path': '/v1/expenses/{date}', 'description': 'Самая затратная категория'},
            {'method': 'GET', 'path': '/v1/expenses/{category}/{date}',
             'description': 'Самая дорогая покупка'},
            {'method': 'GET', 'path': '/v1/help', 'description': 'Справка по API'}
        ]
    }


# Форма запроса для add
class AddExpenseRequestModel(BaseModel):
    expense: str
    category: str
    amount: str
    date: str


# Эндпоинт для добавления трат
@app.post('/v1/expenses')
async def add_expense(request: AddExpenseRequestModel, response: Response):
    """Добавляет новую трату."""
    success_code = budget.add_expense(
        request.expense,
        request.category,
        request.amount,
        request.date
    )

    success_messages = {
        0: 'Ошибка: неправильный тип даты. (должно быть "[день].[месяц]")',
        1: 'Ошибка: неправильная цена. (должна быть числом)',
        2: 'Трата добавлена успешно'
    }

    response_result = 'SUCCESS'
    if success_code != 2:
        response_result = 'FAILURE'
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    return {'result': response_result, 'message': success_messages[success_code]}


# Эедпоинт возвращает самую затратную категорию за указанную дату
@app.get('/v1/expenses/{date}')
async def most_expensive_category(date: str, response: Response):
    """Возвращает самую затратную категорию за указанную дату."""
    result = budget.get_the_most_expensive_category(date)
    response_result = 'SUCCESS'
    if not result:
        response_result = 'FAILURE'
        response.status_code = status.HTTP_404_NOT_FOUND
    return {'result': response_result, 'category': result, 'date': date}


# Эндпоинт возвращает самую дорогую попкупку в указанной категории за указанную дату
@app.get('/v1/expenses/{category}/{date}')
async def most_expensive_purchase(category: str, date: str, response: Response):
    """Возвращает самую дорогую покупку в категории за указанную дату."""
    result = budget.get_the_most_expensive_purchase(category, date)
    response_result = 'SUCCESS'
    if not result:
        response_result = 'FAILURE'
        response.status_code = status.HTTP_404_NOT_FOUND
    return {'result': response_result, 'purchase': result, 'category': category, 'date': date}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8787,
        reload=True
    )

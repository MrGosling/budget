import json
from urllib.parse import unquote


def handle_root(handler):
    handler._send_json("Добро пожаловать в Expense Tracker API")


def handle_healthcheck(handler):
    handler._send_json("OK")


def handle_help(handler):
    handler._send_json({
        "commands": [
            "/api/v1/expenses [POST] - добавить расход",
            "/api/v1/expenses/max_category/{month} [GET] - самая затратная категория за месяц",
            "/api/v1/expenses/{category}/max/{month} [GET] - самая дорогая покупка в категории за месяц"
        ]
    })


def handle_max_category(handler, month):
    if not month.isdigit() or not (1 <= int(month) <= 12):
        return handler._send_json({
            "detail": {
                "loc": ["path", 0],
                "msg": "Некорректный месяц",
                "type": "value_error",
            }
        }, status=422)
    month_str = str(int(month)).zfill(2)
    result = handler.budget.get_the_most_expensive_category(month_str)
    if result is None:
        handler._send_json({"message": "Данные за этот месяц не найдены"}, status=404)
    else:
        handler._send_json(result)


def handle_max_purchase(handler, category_encoded, month):
    category = unquote(category_encoded)
    if not month.isdigit() or not (1 <= int(month) <= 12):
        return handler._send_json({
            "detail": {
                "loc": ["path", 0],
                "msg": "Некорректный месяц",
                "type": "value_error",
            }
        }, status=422)
    month_str = str(int(month)).zfill(2)
    result = handler.budget.get_the_most_expensive_purchase(category, month_str)
    if result is None:
        handler._send_json({"message": "Данные за этот месяц и категорию не найдены"}, status=404)
    else:
        handler._send_json(result)


def handle_add_expense(handler):
    content_length = int(handler.headers.get('Content-Length', 0))
    body = handler.rfile.read(content_length)
    try:
        data = json.loads(body)
    except Exception:
        return handler._send_json({
            "detail": {
                "loc": ["body", 0],
                "msg": "Некорректный JSON",
                "type": "value_error",
            }
        }, status=422)

    required_fields = ("expense", "category", "amount", "date")
    if not all(k in data for k in required_fields):
        return handler._send_json({
            "detail": {
                "loc": ["body", 0],
                "msg": "Отсутствуют обязательные поля",
                "type": "value_error",
            }
        }, status=422)

    result_code = handler.budget.add_expense(
        data["expense"], data["category"], data["amount"], data["date"]
    )
    messages = {
        0: "Ошибка: неверный формат даты или день превышает допустимый",
        1: "Ошибка: сумма должна быть числом",
        2: "Трата успешно добавлена",
    }
    status = 200 if result_code == 2 else 422
    handler._send_json({"message": messages.get(result_code, "Неизвестная ошибка")}, status=status)

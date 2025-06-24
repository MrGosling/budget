import json
import re

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

from budget import Budget


class BudgetHandler(BaseHTTPRequestHandler):
    budget = Budget()

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        # Преобразуем словарь или список в JSON, иначе оборачиваем в {"message": ...}
        if isinstance(data, (dict, list)):
            output = json.dumps(data, ensure_ascii=False)
        else:
            output = json.dumps({"message": data}, ensure_ascii=False)
        self.wfile.write(output.encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self._send_json("Добро пожаловать в Expense Tracker API")
            return

        if path == '/api/v1/healthcheck':
            self._send_json("OK")
            return

        if path == '/api/v1/help':
            help_text = {
                "commands": [
                    "/api/v1/expenses [POST] - добавить расход",
                    "/api/v1/expenses/max_category/{month} [GET] - "
                    "самая затратная категория за месяц",
                    "/api/v1/expenses/{category}/max/{month} [GET] - "
                    "самая дорогая покупка в категории за месяц"
                ]
            }
            self._send_json(help_text)
            return

        # /api/v1/expenses/max_category/{month}
        m = re.match(r'^/api/v1/expenses/max_category/(\d{1,2})$', path)
        if m:
            month = m.group(1)
            if not month.isdigit() or not (1 <= int(month) <= 12):
                self._send_json(
                    {
                        "detail": {
                            "loc": ["path", 0],
                            "msg": "Некорректный месяц",
                            "type": "value_error",
                        }
                    },
                    status=422,
                )
                return
            month_str = str(int(month)).zfill(2)
            result = self.budget.get_the_most_expensive_category(month_str)
            if result is None:
                self._send_json(
                    {"message": "Данные за этот месяц не найдены"}, status=404
                )
            else:
                self._send_json(result)
            return

        # /api/v1/expenses/{category}/max/{month}
        m = re.match(r'^/api/v1/expenses/([^/]+)/max/(\d{1,2})$', path)
        if m:
            category_encoded, month = m.group(1), m.group(2)
            category = unquote(category_encoded)
            if not month.isdigit() or not (1 <= int(month) <= 12):
                self._send_json(
                    {
                        "detail": {
                            "loc": ["path", 0],
                            "msg": "Некорректный месяц",
                            "type": "value_error",
                        }
                    },
                    status=422,
                )
                return
            month_str = str(int(month)).zfill(2)
            result = self.budget.get_the_most_expensive_purchase(category, month_str)
            if result is None:
                self._send_json(
                    {"message": "Данные за этот месяц и категорию не найдены"},
                    status=404,
                )
            else:
                self._send_json(result)
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/v1/expenses':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
            except Exception:
                self._send_json(
                    {
                        "detail": {
                            "loc": ["body", 0],
                            "msg": "Некорректный JSON",
                            "type": "value_error",
                        }
                    },
                    status=422,
                )
                return

            required_fields = ("expense", "category", "amount", "date")
            if not all(k in data for k in required_fields):
                self._send_json(
                    {
                        "detail": {
                            "loc": ["body", 0],
                            "msg": "Отсутствуют обязательные поля",
                            "type": "value_error",
                        }
                    },
                    status=422,
                )
                return

            expense = data["expense"]
            category = data["category"]
            amount = data["amount"]
            date = data["date"]

            # Вызываем метод add_expense из Budget
            success_code = self.budget.add_expense(expense, category, amount, date)
            messages = {
                0: "Ошибка: неверный формат даты или день превышает допустимый",
                1: "Ошибка: сумма должна быть числом",
                2: "Трата успешно добавлена",
            }
            status = 200 if success_code == 2 else 422
            self._send_json({"message": messages.get(success_code, "Неизвестная ошибка")}, status=status)
            return

        self.send_error(404, "Not Found")


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    server = ThreadingHTTPServer((host, port), BudgetHandler)
    print(f"Server running at http://{host}:{port}")
    server.serve_forever()

import pytest
from unittest.mock import Mock
import request_handlers


@pytest.fixture
def mock_handler():
    handler = Mock()
    handler._send_json = Mock()
    handler.budget = Mock()
    handler.headers = {"Content-Length": "0"}
    handler.rfile.read.return_value = b''
    return handler


def test_handle_root(mock_handler):
    request_handlers.handle_root(mock_handler)
    mock_handler._send_json.assert_called_once_with("Добро пожаловать в Expense Tracker API")


def test_handle_healthcheck(mock_handler):
    request_handlers.handle_healthcheck(mock_handler)
    mock_handler._send_json.assert_called_once_with("OK")


def test_handle_help(mock_handler):
    request_handlers.handle_help(mock_handler)
    mock_handler._send_json.assert_called_once()
    assert "commands" in mock_handler._send_json.call_args[0][0]


@pytest.mark.parametrize("month", ["0", "13", "abc"])
def test_handle_max_category_invalid_month(mock_handler, month):
    request_handlers.handle_max_category(mock_handler, month)
    args, kwargs = mock_handler._send_json.call_args
    assert kwargs["status"] == 422
    assert args[0]["detail"]["msg"] == "Некорректный месяц"


def test_handle_max_category_no_data(mock_handler):
    mock_handler.budget.get_the_most_expensive_category.return_value = None
    request_handlers.handle_max_category(mock_handler, "5")
    mock_handler._send_json.assert_called_once_with(
        {"message": "Данные за этот месяц не найдены"}, status=404
    )


def test_handle_max_category_success(mock_handler):
    mock_handler.budget.get_the_most_expensive_category.return_value = {"category": "еда"}
    request_handlers.handle_max_category(mock_handler, "5")
    mock_handler._send_json.assert_called_once_with({"category": "еда"})


@pytest.mark.parametrize("month", ["0", "13", "abc"])
def test_handle_max_purchase_invalid_month(mock_handler, month):
    request_handlers.handle_max_purchase(mock_handler, "еда", month)
    args, kwargs = mock_handler._send_json.call_args
    assert kwargs["status"] == 422
    assert args[0]["detail"]["msg"] == "Некорректный месяц"


def test_handle_max_purchase_no_data(mock_handler):
    mock_handler.budget.get_the_most_expensive_purchase.return_value = None
    request_handlers.handle_max_purchase(mock_handler, "еда", "5")
    mock_handler._send_json.assert_called_once_with(
        {"message": "Данные за этот месяц и категорию не найдены"}, status=404
    )


def test_handle_max_purchase_success(mock_handler):
    mock_handler.budget.get_the_most_expensive_purchase.return_value = {"expense": "стейк"}
    request_handlers.handle_max_purchase(mock_handler, "еда", "5")
    mock_handler._send_json.assert_called_once_with({"expense": "стейк"})


def test_handle_add_expense_invalid_json(mock_handler):
    mock_handler.headers["Content-Length"] = "10"
    mock_handler.rfile.read.return_value = b'{not json}'
    request_handlers.handle_add_expense(mock_handler)
    args, kwargs = mock_handler._send_json.call_args
    assert kwargs["status"] == 422
    assert args[0]["detail"]["msg"] == "Некорректный JSON"


def test_handle_add_expense_missing_fields(mock_handler):
    mock_handler.headers["Content-Length"] = "20"
    mock_handler.rfile.read.return_value = b'{"expense": "x"}'
    request_handlers.handle_add_expense(mock_handler)
    args, kwargs = mock_handler._send_json.call_args
    assert kwargs["status"] == 422
    assert args[0]["detail"]["msg"] == "Отсутствуют обязательные поля"


@pytest.mark.parametrize("code,status,message", [
    (0, 422, "Ошибка: неверный формат даты или день превышает допустимый"),
    (1, 422, "Ошибка: сумма должна быть числом"),
    (2, 200, "Трата успешно добавлена"),
    (999, 422, "Неизвестная ошибка"),
])


def test_handle_add_expense_result_codes(mock_handler, code, status, message):
    mock_handler.headers["Content-Length"] = "100"
    payload = {
        "expense": "кофе",
        "category": "еда",
        "amount": "150",
        "date": "2025-06-22"
    }
    mock_handler.rfile.read.return_value = str.encode(str(payload).replace("'", '"'))
    mock_handler.budget.add_expense.return_value = code

    request_handlers.handle_add_expense(mock_handler)
    mock_handler._send_json.assert_called_once_with({"message": message}, status=status)

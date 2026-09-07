import pytest
import requests
import allure
from utils.helpers import BASE_URL


class TestOrdersList:
    @allure.title("Список заказов: проверка структуры ответа")
    def test_orders_list_returns_list(self):
        response = requests.get(f"{BASE_URL}/orders", timeout=120)
        assert response.status_code == 200
        json_data = response.json()
        assert "orders" in json_data
        assert isinstance(json_data["orders"], list)

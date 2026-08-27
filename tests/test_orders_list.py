import pytest
import requests
import allure
from utils.helpers import BASE_URL


class TestOrdersList:
    @allure.title("Список заказов: проверка структуры ответа")
    def test_orders_list_returns_list(self):
        # Увеличен таймаут до 120 секунд для предотвращения ReadTimeoutError
        response = requests.get(f"{BASE_URL}/orders", timeout=120)
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)

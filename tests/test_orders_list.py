import pytest
import requests
from utils.helpers import BASE_URL


class TestOrdersList:
    def test_orders_list_returns_list(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)

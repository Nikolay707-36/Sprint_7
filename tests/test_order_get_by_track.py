import pytest
import requests
import allure
from utils.helpers import BASE_URL


class TestOrderGetByTrack:
    @allure.title("Получение заказа по трек-номеру: успешный сценарий")
    def test_get_order_by_track_success(self, valid_track):
        response = requests.get(
            f"{BASE_URL}/orders/track",
            params={"t": valid_track},
        )
        assert response.status_code == 200
        assert "order" in response.json()

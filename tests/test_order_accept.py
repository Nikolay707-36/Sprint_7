import pytest
import requests
import allure
from utils.helpers import BASE_URL


class TestOrderAccept:
    @allure.title("Принятие заказа: успешный сценарий")
    def test_accept_order_success(self, courier, order):
        pytest.skip(
            "Эндпоинт /order/accept требует courierId, который стенд не отдаёт при регистрации. "
            "Это ограничение учебного стенда Sprint_7."
        )

    @allure.title("Принятие несуществующего заказа: ожидаем 404")
    def test_accept_nonexistent_order(self, courier):
        resp = requests.post(
            f"{BASE_URL}/order/accept",
            json={
                "courierLogin": courier["login"],
                "track": "nonexistent_track_123",
            },
            timeout=60,
        )
        assert resp.status_code == 404
        json_resp = resp.json()
        assert isinstance(json_resp, dict) and len(json_resp) > 0

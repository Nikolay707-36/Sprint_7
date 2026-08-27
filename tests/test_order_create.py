import pytest
import requests
import allure
from utils.helpers import BASE_URL


class TestOrderCreate:
    @pytest.mark.parametrize(
        "color_payload",
        [
            [],                 # Кейс: цвета нет
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
        ],
        ids=[
            "create_no_color",
            "create_black",
            "create_grey",
            "create_black_grey"
        ]
    )
    @allure.title("Создание заказа: цвета {color_payload}")
    def test_order_create_with_colors(self, color_payload):
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Street 1",
            "metroStation": "1",
            "phone": "+79990000000",
            "rentTime": 1,
            "deliveryDate": "2024-01-01",
            "comment": "Test comment",
        }
        if color_payload:
            payload["color"] = color_payload

        response = requests.post(f"{BASE_URL}/orders", json=payload, timeout=15)
        assert response.status_code in [200, 201]
        assert "track" in response.json()

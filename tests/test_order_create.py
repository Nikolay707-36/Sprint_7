import pytest
import requests
from utils.helpers import BASE_URL


class TestOrderCreate:
    @pytest.mark.parametrize(
        "color_payload",
        [
            None,
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
        ],
    )
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
        if color_payload is not None:
            payload["color"] = color_payload

        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code in (200, 201)
        assert "track" in response.json()

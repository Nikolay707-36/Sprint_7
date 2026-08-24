import pytest
import requests
from utils.helpers import BASE_URL


class TestOrderGetByTrack:
    @pytest.fixture(scope="function")
    def valid_track(self):
        payload = {
            "firstName": "Track",
            "lastName": "Test",
            "address": "Street 3",
            "metroStation": "3",
            "phone": "+79992222222",
            "rentTime": 1,
            "deliveryDate": "2024-01-03",
        }
        resp = requests.post(f"{BASE_URL}/orders", json=payload)
        assert resp.status_code in (200, 201)
        return resp.json()["track"]

    def test_get_order_by_track_success(self, valid_track):
        response = requests.get(
            f"{BASE_URL}/orders/track",
            params={"t": valid_track},
        )
        assert response.status_code == 200
        assert "order" in response.json()

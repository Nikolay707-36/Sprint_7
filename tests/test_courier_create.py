import pytest
import requests
from utils.helpers import generate_random_string, BASE_URL


class TestCourierCreate:
    @pytest.mark.parametrize(
        "payload,expected_status,expected_ok",
        [
            (
                {
                    "login": generate_random_string(10),
                    "password": generate_random_string(10),
                    "firstName": generate_random_string(10),
                },
                201,
                True,
            ),
            ({"login": "", "password": "123", "firstName": "Name"}, 400, None),
            ({"password": "123", "firstName": "Name"}, 400, None),
            ({"login": "test", "firstName": "Name"}, 400, None),
        ],
    )
    def test_create_courier(self, payload, expected_status, expected_ok):
        response = requests.post(f"{BASE_URL}/courier", data=payload)  # data, не json
        assert response.status_code == expected_status
        if expected_ok is not None:
            assert response.json().get("ok") == expected_ok

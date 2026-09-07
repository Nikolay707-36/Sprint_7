import pytest
import requests
import allure
from utils.helpers import BASE_URL, generate_random_string


class TestCourierCreate:
    @pytest.mark.parametrize(
        "payload, expected_status, expect_ok_field",
        [
            # Успешный кейс
            (
                {
                    "login": generate_random_string(10),
                    "password": generate_random_string(10),
                    "firstName": generate_random_string(10),
                },
                201,
                True,
            ),
            # Ошибки валидации (пустой логин)
            ({"login": "", "password": "123", "firstName": "Name"}, 400, False),
            # Ошибки валидации (нет логина)
            ({"password": "123", "firstName": "Name"}, 400, False),
            # Ошибки валидации (нет пароля)
            ({"login": "test", "firstName": "Name"}, 400, False),
        ],
        ids=[
            "create_success",
            "create_empty_login",
            "create_no_login",
            "create_no_password",
        ],
    )
    @allure.title("Создание курьера: статус {expected_status} (кейс: {payload})")
    def test_create_courier(self, payload, expected_status, expect_ok_field):
        response = requests.post(f"{BASE_URL}/courier", data=payload, timeout=15)

        assert response.status_code == expected_status

        json_resp = response.json()

        if expect_ok_field:
            # Для успеха проверяем, что ok есть и он True
            assert "ok" in json_resp
            assert json_resp["ok"] is True
        else:
            # Для ошибок проверяем, что ok либо False, либо отсутствует
            if "ok" in json_resp:
                assert json_resp["ok"] is False
            # Если ok нет — это тоже валидное поведение для ошибки

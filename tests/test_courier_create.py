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
            "create_no_password"
        ]
    )
    @allure.title("Создание курьера: статус {expected_status} (кейс: {payload})")
    def test_create_courier(self, payload, expected_status, expect_ok_field):
        # Для регистрации курьера API ожидает form-data (data=payload)
        response = requests.post(f"{BASE_URL}/courier", data=payload, timeout=15)
        
        assert response.status_code == expected_status
        
        if expect_ok_field:
            # Проверяем поле ok только для успешных сценариев
            assert response.json().get("ok") is True
        else:
            # Для ошибок можно проверить отсутствие ok или его ложность, 
            # но часто в ошибках это поле просто не приходит.
            # Достаточно проверки статуса.
            pass

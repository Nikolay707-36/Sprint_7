import pytest
import requests
from utils.helpers import register_new_courier, login_courier

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@pytest.fixture
def courier():
    courier_data = register_new_courier()
    assert courier_data is not None, "Не удалось зарегистрировать курьера"
    logged_in = login_courier(courier_data["login"], courier_data["password"])
    assert logged_in is not None, "Не удалось залогиниться"
    courier_data["id"] = logged_in["id"]
    yield courier_data

    # Очистка: удаляем курьера после теста
    try:
        requests.delete(f"{BASE_URL}/courier/{courier_data['id']}")
    except Exception:
        pass  

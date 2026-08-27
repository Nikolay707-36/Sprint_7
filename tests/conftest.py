import pytest
import requests
import time
from utils.helpers import BASE_URL, register_new_courier, login_courier

@pytest.fixture
def courier():
    login = f"courier_{int(time.time() * 1000)}"
    password = "12345"
    first_name = "Test"

    reg_payload = {
        "firstName": first_name,
        "lastName": "Courier",
        "login": login,
        "password": password,
        "role": "courier",
    }

    # Используем data= для регистрации (form-data), как требует API
    reg_resp = register_new_courier(reg_payload)
    
    if reg_resp.status_code not in (201, 200):
        pytest.fail(f"Регистрация курьера не удалась: status={reg_resp.status_code}, body={reg_resp.text}")

    # Логинимся, чтобы убедиться, что курьер создан
    login_payload = {"login": login, "password": password}
    login_resp = login_courier(login_payload)
    
    if login_resp.status_code != 200:
        pytest.fail(f"Не удалось залогиниться: status={login_resp.status_code}, body={login_resp.text}")

    courier_obj = {
        "login": login,
        "password": password,
    }

    yield courier_obj

    # Очистка (не должна ломать тест, если стенд не поддерживает удаление)
    try:
        delete_resp = requests.delete(f"{BASE_URL}/courier?login={login}", timeout=10)
        if delete_resp.status_code not in (200, 204, 404):
            print(f"Warning: courier delete returned {delete_resp.status_code}")
    except Exception as e:
        print(f"Warning: exception during courier cleanup: {e}")


@pytest.fixture
def valid_track():
    """
    Создает заказ и возвращает его track.
    Вынесено из test_order_get_by_track.py в conftest.py.
    """
    payload = {
        "firstName": "Track",
        "lastName": "Test",
        "address": "Street 3",
        "metroStation": "3",
        "phone": "+79992222222",
        "rentTime": 1,
        "deliveryDate": "2024-01-03",
    }
    # Увеличиваем таймаут для создания заказа, чтобы избежать случайных таймаутов
    resp = requests.post(f"{BASE_URL}/orders", json=payload, timeout=60)
    
    if resp.status_code not in (200, 201):
        pytest.fail(f"Не удалось создать заказ для фикстуры valid_track: status={resp.status_code}, body={resp.text}")
    
    try:
        return resp.json()["track"]
    except KeyError:
        pytest.fail(f"Ответ сервера не содержит поле 'track': {resp.text}")


@pytest.fixture
def order(courier):
    """
    Фикстура для создания заказа.
    Возвращает словарь с данными заказа, включая track.
    """
    payload = {
        "firstName": "Order",
        "lastName": "Test",
        "address": "Street 5",
        "metroStation": "5",
        "phone": "+79995555555",
        "rentTime": 1,
        "deliveryDate": "2024-01-05",
    }
    
    # Создаем заказ
    resp = requests.post(f"{BASE_URL}/orders", json=payload, timeout=60)
    
    if resp.status_code not in (200, 201):
        pytest.fail(f"Не удалось создать заказ для фикстуры order: status={resp.status_code}, body={resp.text}")
    
    try:
        data = resp.json()
        order_data = {
            "track": data["track"],
            "id": data.get("id"),
            "status": data.get("status")
        }
        return order_data
    except KeyError:
        pytest.fail(f"Ответ сервера не содержит необходимые поля: {resp.text}")

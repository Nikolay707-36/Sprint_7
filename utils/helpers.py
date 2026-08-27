import requests
import random
import string


BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))

def register_new_courier(payload: dict) -> requests.Response:
    """
    Регистрирует курьера.
    Важно: API ожидает form-data, поэтому используем data=payload.
    """
    return requests.post(f"{BASE_URL}/courier", data=payload, timeout=15)

def login_courier(payload: dict) -> requests.Response:
    """
    Логинит курьера.
    API ожидает JSON, поэтому используем json=payload.
    """
    return requests.post(f"{BASE_URL}/courier/login", json=payload, timeout=15)

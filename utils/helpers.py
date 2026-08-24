import requests
import random
import string


BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))

def register_new_courier() -> dict | None:
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    # Важно: для регистрации API ожидает данные как form-data (data=payload), а не json
    response = requests.post(f"{BASE_URL}/courier", data=payload)
    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "first_name": first_name,
            "id": None,
        }
    return None

def login_courier(login: str, password: str) -> dict | None:
    payload = {"login": login, "password": password}
    # Для логина API ожидает JSON (json=payload)
    response = requests.post(f"{BASE_URL}/courier/login", json=payload)
    if response.status_code == 200:
        data = response.json()
        return {"id": data.get("id"), "login": login, "password": password}
    return None

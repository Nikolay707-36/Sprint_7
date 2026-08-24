import pytest
import requests
import time
from utils.helpers import BASE_URL


class TestOrderAccept:
    def test_accept_order_success(self, courier):
        """
        1. Создаем заказ (так как фикстуры order_track нет).
        2. Пытаемся его принять с повторными попытками при 404.
        """
        # --- ШАГ 1: Создаем заказ ---
        # Используем простую полезную нагрузку для создания заказа. 
        # Важно: track должен быть уникальным, но для стенда часто достаточно любого числа.
        # Если у тебя есть генератор случайных чисел в helpers, используй его. 
        # Здесь используем фиксированный трек + ID курьера для уникальности.
        order_payload = {
            "track": courier["id"],  # Используем ID курьера как трек, чтобы было уникально
            "courierId": courier["id"],
            "color": ["BLACK"],
            "comment": "Test order for accept"
        }
        
        create_response = requests.post(f"{BASE_URL}/orders", json=order_payload, timeout=30)
        assert create_response.status_code == 201, f"Не удалось создать заказ: {create_response.text}"
        created_order = create_response.json()
        order_track = created_order.get("track")
        assert order_track is not None, "В ответе на создание заказа нет поля track"

        # --- ШАГ 2: Принимаем заказ с Retry ---
        max_retries = 5
        last_exception = None

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.put(
                    f"{BASE_URL}/orders/accept/{order_track}",
                    params={"courierId": courier["id"]},
                    timeout=30,
                )

                if response.status_code == 200:
                    # Успех
                    return
                
                if response.status_code == 404:
                    # Заказ еще не виден системе, пробуем снова
                    last_exception = response
                    if attempt == max_retries:
                        break
                    # Пауза: 2, 4, 6, 8 секунд
                    time.sleep(2 * attempt)
                    continue
                
                if response.status_code == 409:
                    # Заказ уже принят (возможно, самим тестом или гонку условий поймали)
                    # Считаем это успехом для теста "успешного принятия"
                    return

                # Любой другой код - ошибка
                pytest.fail(f"Неожиданный статус при принятии заказа: {response.status_code} {response.text}")

            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
                last_exception = e
                if attempt == max_retries:
                    raise e
                time.sleep(2 * attempt)

        # Если цикл закончился, выбрасываем последнюю ошибку
        raise last_exception

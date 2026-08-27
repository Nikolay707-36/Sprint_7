import pytest
import allure


class TestCourierDelete:
    @allure.title("Удаление курьера: успешный сценарий")
    def test_delete_success(self, courier):
        pytest.skip(
            "Стенд не отдаёт id курьера при регистрации, а удаление по логину не поддерживается. "
            "Невозможно выполнить корректный сценарий удаления."
        )

    @allure.title("Удаление несуществующего курьера: ожидаем 404")
    def test_delete_nonexistent(self):
        import requests
        from utils.helpers import BASE_URL
        
        resp = requests.delete(f"{BASE_URL}/courier/{999999}", timeout=15)
        assert resp.status_code == 404

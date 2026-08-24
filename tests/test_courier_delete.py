import pytest
import requests
from utils.helpers import BASE_URL, register_new_courier, login_courier

class TestCourierDelete:
    @pytest.fixture(scope="function")
    def courier_with_id(self):
        courier = register_new_courier()
        logged = login_courier(courier["login"], courier["password"])
        courier["id"] = logged["id"]
        yield courier

    def test_delete_success(self, courier_with_id):
        response = requests.delete(f"{BASE_URL}/courier/{courier_with_id['id']}")
        assert response.status_code == 200
        assert response.json().get("ok") is True

    @pytest.mark.parametrize("id_value", [999999])
    def test_delete_nonexistent(self, id_value):
        response = requests.delete(f"{BASE_URL}/courier/{id_value}")
        assert response.status_code == 400 or response.status_code == 404

import allure
import pytest
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("User Deletion Tests")
class TestUserDelete(BaseCase):

    # Первый тест - попытка удалить пользователя с ID 2
    @allure.description("This test verifies that user with ID 2 can't be deleted")
    def test_delete_user_2(self):
        # Данные для авторизации
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # Авторизация пользователя
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Попытка удаления пользователя с ID 2
        response2 = MyRequests.delete("/user/2", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        assert response2.status_code == 400, f"Unexpected status code {response2.status_code}"

    # Второй тест - создание, авторизация и удаление пользователя
    @allure.description("This test verifies that a user can be deleted successfully")
    def test_positive_delete_created_user(self):
        # Регистрация нового пользователя
        registration_data = self.preapare_registration_data()
        response1 = MyRequests.post("/user/", data=registration_data)
        user_id = self.get_json_value(response1, "id")

        # Авторизация пользователя
        response2 = MyRequests.post("/user/login", data={'email': registration_data['email'],
                                                         'password': registration_data['password']})
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удаление пользователя
        response3 = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        assert response3.status_code == 200, f"Unexpected status code {response3.status_code}"

        # Проверка, что пользователь действительно удален
        response4 = MyRequests.get(f"/user/{user_id}")
        assert response4.status_code == 404, f"Unexpected status code {response4.status_code}"

    # Третий тест - попытка удалить одного пользователя, будучи авторизованным другим пользователем
    @pytest.mark.xfail(reason="This test is expected to fail due to a known defect")
    @allure.description("This test verifies that one user cannot delete another user")
    def test_delete_user_authorized_as_another_user(self):
        # Создание двух пользователей
        first_user_data = self.preapare_registration_data()
        response_first_user = MyRequests.post("/user/", data=first_user_data)
        first_user_id = self.get_json_value(response_first_user, "id")
        second_user_data = self.preapare_registration_data()
        MyRequests.post("/user/", data=second_user_data)

        # Авторизация под вторым пользователем
        response1 = MyRequests.post("/user/login",
                                    data={'email': second_user_data['email'], 'password': second_user_data['password']})
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Попытка удалить первого пользователя из-под учетной записи второго пользователя
        response2 = MyRequests.delete(f"/user/{first_user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        assert response2.status_code == 400, f"Unexpected status code {response2.status_code}"
        # Проверка, что пользователь действительно не был удален
        response_check = MyRequests.get(f"/user/{first_user_id}")
        assert response_check.status_code == 200, f"User was actually deleted! Status code: {response_check.status_code}"

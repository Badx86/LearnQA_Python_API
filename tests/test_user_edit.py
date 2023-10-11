import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User Edit Functionality")
class TestUserEdit(BaseCase):
    """
    Класс для тестирования функционала редактирования пользователя
    """

    # REGISTER
    @allure.description("This test verifies the ability to edit a user after their registration")
    def test_edit_just_created_user(self):
        """
        Тест проверяет возможность редактирования пользователя после его регистрации
        """
        # Генерируем данные для регистрации пользователя
        register_data = self.preapare_registration_data()
        # Отправляем запрос на регистрацию пользователя
        response1 = MyRequests.post("/user/", data=register_data)
        # Проверяем корректность ответа после регистрации
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        # Извлекаем необходимые данные для авторизации
        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        # Формируем данные для авторизации
        login_data = {
            'email': email,
            'password': password
        }
        # Отправляем запрос на авторизацию пользователя
        response2 = MyRequests.post("/user/login", data=login_data)
        # Извлекаем данные для следующего этапа (редактирования)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        # Формируем новое имя для редактирования пользователя
        new_name = "Changed Name"
        # Отправляем запрос на редактирование пользователя
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        # Проверяем корректность ответа после редактирования
        Assertions.assert_code_status(response3, 200)

        # GET
        # Отправляем запрос на получение данных пользователя
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        # Проверяем, что имя пользователя изменилось
        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit"
                                             )

    @allure.description("This test checks the inability to edit a user when unauthorized")
    def test_edit_user_unauthorized(self):
        # Генерируем данные для регистрации пользователя
        register_data = self.preapare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response1, "id")
        new_name = "Changed Name Unauth"
        # Отправляем запрос на редактирование пользователя без авторизации
        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == "Auth token not supplied", f"Unexpected response content {response2.content}"

    @pytest.mark.xfail(reason="API allows unauthorized edits. Needs to be fixed.")
    @allure.description("This test checks the inability to edit a user when authorized as another user")
    def test_edit_user_authorized_as_another_user(self):
        # Создаем первого пользователя
        first_user_data = self.preapare_registration_data()
        response1 = MyRequests.post("/user/", data=first_user_data)
        first_user_id = self.get_json_value(response1, "id")

        # Создаем второго пользователя и авторизуемся
        second_user_data = self.preapare_registration_data()
        MyRequests.post("/user/", data=second_user_data)
        login_data = {
            'email': second_user_data['email'],
            'password': second_user_data['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # Попытка редактирования первого пользователя от имени второго
        new_name = "Changed Name By Another User"
        response4 = MyRequests.put(f"/user/{first_user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        # Ожидаем ошибку, так как это не должно быть разрешено
        # Попытка редактирования данных другого пользователя должна завершиться ошибкой
        Assertions.assert_code_status(response4, 400)
        # Убеждаемся, что имя первого пользователя не изменилось
        response5 = MyRequests.get(f"/user/{first_user_id}")
        # print(response5.json())
        Assertions.assert_json_value_by_name(response5, "firstName", first_user_data['firstName'],
                                             "Name of the first user was changed.")

    @allure.description("This test checks the inability to change user email to an invalid one")
    def test_edit_user_invalid_email(self):
        # Регистрируем и авторизуем пользователя
        user_data = self.preapare_registration_data()
        response1 = MyRequests.post("/user/", data=user_data)
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Попытка изменить email
        invalid_email = "invalidemail.com"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": invalid_email}
                                   )
        Assertions.assert_code_status(response3, 400)

    @allure.description("This test checks the inability to change user first name to a very short value")
    def test_edit_user_short_first_name(self):
        # Регистрируем и авторизуем пользователя
        user_data = self.preapare_registration_data()
        response1 = MyRequests.post("/user/", data=user_data)
        user_id = self.get_json_value(response1, "id")
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Попытка изменить имя на один символ
        short_name = "A"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": short_name}
                                   )
        Assertions.assert_code_status(response3, 400)

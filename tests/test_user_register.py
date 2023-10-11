from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User Registration Functionality")
class TestUserRegister(BaseCase):

    @allure.description("This test verifies that a user can be created successfully")
    def test_create_user_successfully(self):
        data = self.preapare_registration_data()
        # Отправка POST запроса для регистрации пользователя
        response = MyRequests.post("/user/", data=data)
        # Проверка кода ответа и наличия ключа "id" в ответе
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test checks the registration of a user with an already existing email")
    def test_create_user_with_existing_email(self):
        """
        Тестирование регистрации пользователя с существующим email
        """
        email = 'test@example.com'
        data = self.preapare_registration_data(email)
        # Отправка POST запроса для регистрации пользователя
        response = MyRequests.post("/user/", data=data)
        # Проверка кода ответа и содержимого ответа
        Assertions.assert_code_status(response, 400)
        assert response.text == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

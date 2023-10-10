import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.preapare_registration_data()
        # Отправка POST запроса для регистрации пользователя
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        # Проверка кода ответа и наличия ключа "id" в ответе
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        """
        Тестирование регистрации пользователя с существующим email
        """
        email = 'test@example.com'
        data = self.preapare_registration_data(email)
        # Отправка POST запроса для регистрации пользователя
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        # Проверка кода ответа и содержимого ответа
        Assertions.assert_code_status(response, 400)
        assert response.text == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

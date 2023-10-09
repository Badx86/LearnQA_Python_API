import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    """
    Класс для тестирования регистрации пользователя
    """
    def setup_method(self):
        """
            Метод для инициализации начальных значений перед каждым тестом
            Генерирует уникальный email для регистрации пользователя
            """
        base_part = "test"
        domain = "example.com"
        # Генерация уникальной части email на основе текущей даты и времени
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        """
        Тестирование успешной регистрации пользователя.
        """
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'Test',
            'lastName': 'Example',
            'email': self.email
        }
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
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'Test',
            'lastName': 'Example',
            'email': email
        }
        # Отправка POST запроса для регистрации пользователя
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        # Проверка кода ответа и содержимого ответа
        Assertions.assert_code_status(response, 400)
        assert response.text == f"Users with email '{email}' already exists", \
                                f"Unexpected response content {response.content}"

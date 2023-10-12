import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User Registration Tests")
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

    @allure.description("This test checks user registration with an incorrect email w/o '@'")
    def test_create_user_with_invalid_email(self):
        # Подготовка данных с некорректным email (без символа '@')
        data = self.preapare_registration_data(email="testemail.com")
        # Отправка POST запроса для регистрации пользователя
        response = MyRequests.post("/user/", data=data)
        # Проверка кода ответа
        Assertions.assert_code_status(response, 400)

    @allure.description("This test checks user registration without one of the fields")
    @pytest.mark.parametrize('field', ['username', 'password', 'email', 'firstName', 'lastName'])
    def test_create_user_without_field(self, field):
        # Подготовка данных для регистрации пользователя
        data = self.preapare_registration_data()
        # Удаление одного из полей из данных для регистрации
        data.pop(field)
        # Отправка POST запроса для регистрации пользователя
        response = MyRequests.post("/user/", data=data)
        # Проверка кода ответа
        Assertions.assert_code_status(response, 400)

    @allure.description("This test checks user registration with a very short name")
    def test_create_user_with_short_name(self):
        # Подготовка данных с коротким именем пользователя
        data = self.preapare_registration_data(firstName="A")
        # Отправка POST запроса для регистрации пользователя
        response = MyRequests.post("/user/", data=data)
        # Проверка кода ответа
        Assertions.assert_code_status(response, 400)

    @allure.description("This test checks user registration with a very long name")
    def test_create_user_with_long_name(self):
        # Подготовка данных с очень длинным именем пользователя
        name = "A" * 251
        data = self.preapare_registration_data(firstName=name)
        # Отправка POST запроса для регистрации пользователя
        response = MyRequests.post("/user/", data=data)
        # Проверка кода ответа
        Assertions.assert_code_status(response, 400)

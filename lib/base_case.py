import json.decoder
from requests import Response
from datetime import datetime


class BaseCase:
    """
    Базовый класс с вспомогательными методами для тестов
    """
    def get_cookie(self, response: Response, cookie_name):
        """
        Получить значение куки из ответа по имени куки

        :param response: Ответ, из которого необходимо извлечь куку
        :param cookie_name: Имя куки, которую хотим извлечь
        :return: Значение куки
        """
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        """
        Получить значение заголовка из ответа по его имени

        :param response: Ответ, из которого необходимо извлечь заголовок
        :param headers_name: Имя заголовка, которое хотим извлечь
        :return: Значение заголовка
        """
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        """
        Получить значение из JSON-ответа по ключу

        :param response: Ответ в формате JSON
        :param name: Ключ, по которому извлекается значение
        :return: Значение по ключу из JSON
        """
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"

        return response_as_dict[name]

    def preapare_registratrion_data(self, email=None):
        """
        Подготовить данные для регистрации пользователя

        :param email: Электронная почта пользователя. Если None, то будет сгенерирована
        :return: Словарь с данными для регистрации
        """
        if email is None:
            base_part = "test"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'Test',
            'lastName': 'Example',
            'email': email
        }

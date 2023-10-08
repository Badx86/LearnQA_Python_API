import json.decoder
from requests import Response


class BaseCase:
    """
    Базовый класс с вспомогательными методами для тестов
    """
    def get_cookie(self, response: Response, cookie_name):
        """
        Получить определенную куку из ответа
        """
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        """
        Получить определенный заголовок из ответа
        """
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        """
        Получить определенное значение JSON по его имени/ключу из ответа
        """
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"

        return response_as_dict[name]
from requests import Response
import json


class Assertions:
    """
    Вспомогательный класс для проверки различных свойств ответа
    """
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        """
        Проверяет, что ответ содержит JSON и в этом JSON присутствует поле с ожидаемым значением

        :param response: Ответ от сервера
        :param name: Ключ в JSON, который необходимо проверить
        :param expected_value: Ожидаемое значение ключа
        :param error_message: Сообщение об ошибке, которое будет выведено, если проверка не пройдет
        """
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        """
        Проверяет, что ответ содержит JSON и в этом JSON присутствует заданный ключ

        :param response: Ответ от сервера
        :param name: Ключ в JSON, который необходимо проверить
        """
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        """
        Проверяет, что ответ содержит JSON и в этом JSON присутствуют все указанные ключи

        :param response: Ответ от сервера
        :param names: Список ключей, которые должны быть в JSON ответе
        """
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn`t have key '{name}'"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        """
        Проверяет, что ответ содержит JSON и в этом JSON отсутствует заданный ключ

        :param response: Ответ от сервера
        :param name: Ключ в JSON, которого не должно быть в ответе
        """
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response JSON shouldn`t have key '{name}. But it`s present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        """
        Проверяет, что статус ответа соответствует ожидаемому

        :param response: Ответ от сервера
        :param expected_status_code: Ожидаемый статус кода ответа
        """
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"


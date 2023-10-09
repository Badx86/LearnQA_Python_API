import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    """
    Класс тестов для проверки аутентификации пользователя
    """
    # Параметры для негативных сценариев тестирования
    exclude_params = [
        "no_cookie",
        "no_token"
    ]

    def setup_method(self):
        """
        Метод настройки для аутентификации пользователя и установки необходимых токенов и кук
        """
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_auth_user(self):
        """
        Тест для проверки аутентифицированного пользователя
        """
        response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid}
                                 )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        """
        Негативный тест для проверки аутентификации в разных условиях
        """
        if condition == "no_cookie":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )

    def test_short_phrase(self):
        """
        Тест, который запрашивает короткую фразу у пользователя
        """
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "The phrase is longer than 15 characters!"

    def test_cookie(self):
        """
        Тест для проверки установки куки
        """
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie_value = response.cookies.get("HomeWork")
        print(f"Cookie value: {cookie_value}")
        assert cookie_value is not None, "Cookie 'HomeWork' is set!"
        # print(response.text)
        # print(response.headers)
        # print(response.cookies)

    def test_homework_header(self):
        """
        Тест для проверки установки заголовка
        """
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        header_value = response.headers.get("x-secret-homework-header")
        print(f"Header value: {header_value}")
        assert header_value is not None, "Header 'x-secret-homework-header' is not set"

    # Данные для тестирования User Agent
    user_agents_data = [
        (
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),

        (
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),

        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),

        (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),

        (
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
    ]

    failed_agents = []

    @pytest.mark.parametrize('user_agent, expected_values', user_agents_data)
    def test_user_agent_check(self, user_agent, expected_values):
        """
        Тест для проверки корректности определения User Agent
        """
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent}
        )
        actual_values = response.json()

        for key, value in expected_values.items():
            if actual_values.get(key) != value:
                self.failed_agents.append((user_agent, key, value, actual_values.get(key)))

    @pytest.mark.xfail
    def test_summary(self):
        """
        Итоговый тест, который проверяет, были ли ошибки в определении User Agent
        """
        assert len(self.failed_agents) == 0, f"Failed User Agents: {self.failed_agents}"

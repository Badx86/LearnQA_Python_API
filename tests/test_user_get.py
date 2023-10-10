from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    """
    Класс для тестирования получения информации о пользователе
    """

    def test_get_user_details_not_auth(self):
        """
        Тестирование получения информации о пользователе без аутентификации
        """
        # Отправка GET запроса для получения информации о пользователе
        response = MyRequests.get("/user/2")
        # Проверка наличия и отсутствия определенных полей в ответе
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        """
        Тестирование получения информации о пользователе после аутентификации того же пользователя.
        """
        # Данные для аутентификации пользователя
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # Отправка POST запроса для аутентификации пользователя
        response1 = MyRequests.post("/user/login", data=data)
        # Получение данных из ответа для последующего запроса
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        # Отправка GET запроса для получения информации о пользователе с использованием аутентификации
        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        # Проверка наличия определенных полей в ответе
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

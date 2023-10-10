import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    """
    Класс для тестирования функционала редактирования пользователя
    """
    # REGISTER
    def test_edit_just_created_user(self):
        """
        Тест проверяет возможность редактирования пользователя после его регистрации
        """
        # Генерируем данные для регистрации пользователя
        register_data = self.preapare_registration_data()
        # Отправляем запрос на регистрацию пользователя
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
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
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        # Извлекаем данные для следующего этапа (редактирования)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        # Формируем новое имя для редактирования пользователя
        new_name = "Changed Name"
        # Отправляем запрос на редактирование пользователя
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        # Проверяем корректность ответа после редактирования
        Assertions.assert_code_status(response3, 200)

        # GET
        # Отправляем запрос на получение данных пользователя
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        # Проверяем, что имя пользователя изменилось
        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit"
                                             )

import requests
import time

payload = {"login": "secret_login", "password": "secret_pass"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

cookie_value = response.cookies.get("auth_cookie")

cookies = {}
if cookie_value is not None:
    cookies.update({"auth_cookie": cookie_value})

response = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print(response.text)

#  HW
# Ex5
json_text = {"messages": [{"message": "This is the first message", "timestamp": "2021-06-04 16:40:53"},
                          {"message": "And this is a second message", "timestamp": "2021-06-04 16:41:01"}]}
print(json_text["messages"][1]["message"])
# Ex6
response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
redirects_count = len(response.history)
final_url = response.url
print(f"Количество редиректов: {redirects_count}")
print(f"Итоговый URL: {final_url}")
# Ex7
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
response = requests.get(url)
print("1. GET запрос без параметра method:", response.text)

response = requests.head(url)
print("\n2. HEAD запрос:", response.text)
print("Код ответа:", response.status_code)
print("Заголовки ответа:", response.headers)

response = requests.get(url, params={"method": "GET"})
print("\n3. GET запрос с правильным параметром method:", response.text)

methods = ["GET", "POST", "PUT", "DELETE"]
print("\n4. Проверка всех возможных сочетаний:")
for request_method in methods:
    for param_method in methods:
        if request_method == "GET":
            response = requests.get(url, params={"method": param_method})
        else:
            response = requests.request(request_method, url, data={"method": param_method})
        print(f"Запрос методом {request_method} с параметром method={param_method}:", response.text)
# Ex8
# URL API-метода
url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Шаг 1: Создаем задачу
response = requests.get(url)
data = response.json()

# Извлекаем время задержки и токен из ответа
seconds = data["seconds"]
token = data["token"]

print(f"\nЗадача создана! Задержка: {seconds} секунд. Токен: {token}\n")

# Шаг 2: Делаем один запрос с токеном ДО того, как задача готова
response_before = requests.get(url, params={"token": token})
data_before = response_before.json()
print(f"Ответ перед завершением задачи: {data_before}\n")

# Шаг 3: Ждем нужное количество секунд
print(f"Ожидаем {seconds} секунд...")
time.sleep(seconds)

# Шаг 4: Делаем запрос с токеном ПОСЛЕ того, как задача готова
response_after = requests.get(url, params={"token": token})
data_after = response_after.json()
print(f"Ответ после завершения задачи: {data_after}\n")
# Ex9*
# URL-адреса API-методов
password_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

# Логин
login = "super_admin"

# Предполагаемые пароли c https://en.wikipedia.org/wiki/List_of_the_most_common_passwords
passwords = [
    "123456",
    "123456789",
    "12345",
    "qwerty",
    "password",
    "12345678",
    "111111",
    "123123",
    "1234567890",
    "1234567",
    "qwerty123",
    "000000",
    "1q2w3e",
    "aa12345678",
    "abc123",
    "password1",
    "1234",
    "qwertyuiop",
    "123321",
    "password123"
]

# Проверяем каждый пароль
for password in passwords:
    # Запрос к первому методу
    response = requests.post(password_url, data={"login": login, "password": password})

    # Извлекаем куки
    cookie_value = response.cookies.get("auth_cookie")

    if cookie_value:
        # Запрос к второму методу с полученным куком
        response = requests.post(check_auth_url, cookies={"auth_cookie": cookie_value})

        # Проверяем, авторизованы ли мы
        if response.text == "You are NOT authorized":
            print(f"Найден верный пароль: {password}")
            break
        else:
            print(f"Пароль {password} неверный")
    else:
        print(f"Не удалось получить куки для пароля {password}")

# print(response1.status_code)
# print(dict(response1.cookies))

# headers = {"some_header": "123"}
#
# response = requests.post("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
#
# print(response.text)  # запрос
# print(response.headers)  # ответ

import requests

payload = {"login": "secret_login", "password": "secret_pass"}
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

cookie_value = response1.cookies.get("auth_cookie")

cookies = {}
if cookie_value is not None:
    cookies.update({"auth_cookie": cookie_value})

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print(response2.text)

# print(response1.status_code)
# print(dict(response1.cookies))

# headers = {"some_header": "123"}
#
# response = requests.post("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
#
# print(response.text)  # запрос
# print(response.headers)  # ответ



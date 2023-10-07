import requests

headers = {"some_header": "123"}

response = requests.post("https://playground.learnqa.ru/api/show_all_headers", headers=headers)

print(response.text)  # запрос
print(response.headers)  # ответ

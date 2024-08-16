# import requests
# import json
# headers = {
#     'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoicm9vdCJ9.Dw3UeBJHtzF093WGtArcR_sdmvDiVV83QmycU2VIrYA',
#     'username' : 'root'}
# response = requests.get('http://192.168.0.163:8000/free_works', headers = headers)
#
# data = response.json()
#
# # Обрабатываем данные
# print("Статус ответа:", data.get("status"))
# records = data.get("data", [])
# for i in records:
#     print(i)
#
# import requests
# data = {'username': 'root', 'password': 'root'}
# response = requests.post('http://192.168.0.163:8000/login', data=data)
# jwt_token = response.content.decode("utf-8")
# print(jwt_token)
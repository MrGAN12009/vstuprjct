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
#
# import requests
# response = requests.get("http://185.180.109.43:8000")
# print(response.status_code)
import sqlite3


db = sqlite3.connect("test.db")
sql = db.cursor()

sql.execute("""
CREATE TABLE IF NOT EXISTS works(
username VARCHAR(45),
title VARCHAR(45),
forTeacher VARCHAR(45),
course INT,
predmet VARCHAR(45),
isFree BOOLEAN,
grade INT,
text TEXT)""")
db.commit()

sql.execute(f"SELECT * FROM works")
arr = sql.fetchall()

for i in arr:
    if i[1] == 'title1':
        print(i)



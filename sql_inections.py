# import sqlite3
# import json
#
# db = sqlite3.connect("db.db")
# sql = db.cursor()
# sql.execute("""
# CREATE TABLE IF NOT EXISTS numbers(
# name VARCHAR(45),
# phone BIGINT)""")
# db.commit()
#
#
# def post(name, phone):
#     sql.execute(f"INSERT INTO numbers (name, phone) VALUES({name}, {phone})")
#     db.commit()
#     return str(f"{name} - {phone}")
#
#
# def select_one_name(name):
#     sql.execute(f"SELECT name,phone FROM numbers WHERE name = {name}")
#     return sql.fetchone()
#
#
# def select_one_phone(phone):
#     sql.execute(f"SELECT name,phone FROM numbers WHERE phone = {phone}")
#     return sql.fetchone()
#
#
# def select_all():
#     sql.execute(f"SELECT * FROM numbers")
#     return sql.fetchall()
#
# data = {}
# for i in select_all():
#     print(i)
#     data[str(i).split(",")[1].strip()[:-1]] = str(i).split("'")[1]
#
# json.dumps(data)


import requests

def get_external_ip():
    try:
        # Отправляем запрос к сервису, который возвращает внешний IP
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Проверка на успешный ответ
        ip_data = response.json()  # Преобразуем ответ в JSON
        return ip_data['ip']  # Получаем IP-адрес из JSON
    except requests.RequestException as e:
        print(f"Ошибка при получении IP: {e}")
        return None

if __name__ == '__main__':
    ip = get_external_ip()
    if ip:
        print(f"Ваш внешний IP-адрес: {ip}")

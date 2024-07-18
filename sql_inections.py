import sqlite3
import json

db = sqlite3.connect("db.db")
sql = db.cursor()
sql.execute("""
CREATE TABLE IF NOT EXISTS numbers(
name VARCHAR(45),
phone BIGINT)""")
db.commit()


def post(name, phone):
    sql.execute(f"INSERT INTO numbers (name, phone) VALUES({name}, {phone})")
    db.commit()
    return str(f"{name} - {phone}")


def select_one_name(name):
    sql.execute(f"SELECT name,phone FROM numbers WHERE name = {name}")
    return sql.fetchone()


def select_one_phone(phone):
    sql.execute(f"SELECT name,phone FROM numbers WHERE phone = {phone}")
    return sql.fetchone()


def select_all():
    sql.execute(f"SELECT * FROM numbers")
    return sql.fetchall()

data = {}
for i in select_all():
    print(i)
    data[str(i).split(",")[1].strip()[:-1]] = str(i).split("'")[1]

json.dumps(data)
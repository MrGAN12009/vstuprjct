import requests
headers = {'Authorization': f'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoicm9vdCJ9.Dw3UeBJHtzF093WGtArcR_sdmvDiVV83QmycU2VIrYA'}
response = requests.get('http://192.168.0.163:8000/main', headers=headers)

print(response)
r = str(response.content)
print(r)
# import sqlite3
# #sql
# db = sqlite3.connect("db.db")
# sql = db.cursor()
# sql.execute("""
# CREATE TABLE IF NOT EXISTS users(
# username VARCHAR(45),
# password VARCHAR(20))""")
# sql.execute("""
# CREATE TABLE IF NOT EXISTS texts(
# username VARCHAR(45),
# text TEXT)""")
# db.commit()
#
# sql.execute(f"INSERT INTO texts (username, text) VALUES('root', 'rootrootrootroot')")
# sql.execute(f"INSERT INTO users (username, password) VALUES('root', 'root')")
# db.commit()
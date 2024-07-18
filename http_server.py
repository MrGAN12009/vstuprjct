from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import http.client
import json
conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
print(conn.getresponse().read())

#sql
import sqlite3


db = sqlite3.connect("db.db")
sql = db.cursor()
sql.execute("""
CREATE TABLE IF NOT EXISTS numbers(
name VARCHAR(45),
phone BIGINT)""")
db.commit()


def post(name, phone):
    sql.execute(f"INSERT INTO numbers (name, phone) VALUES('{name}', {phone})")
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


#http
class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        data = {}
        for i in select_all():
            data[str(i).split(",")[1].strip()[:-1]] = str(i).split("'")[1]
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data_arr = [i for i in str(post_data)[2:-1].split('=')]




        if select_one_phone(post_data_arr[1]) == None:
            #pass
            pass
        print(post(post_data_arr[0],post_data_arr[1]))




        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"Received POST data: {post_data.decode('utf-8')}"
        print(post_data)
        self.wfile.write(response.encode('utf-8'))


print("Starting server on port 8000...")
server_address = ('', 8000)
httpd = HTTPServer(server_address, HttpGetHandler)
httpd.serve_forever()

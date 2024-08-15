import sqlite3

db = sqlite3.connect("db.db")
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

sql.execute(f"INSERT INTO works(username, title, forTeacher, course, predmet, isFree, grade, text) VALUES('username1', 'title1', 'forteacher1', 1, 'prednet1', True, 91, 'tttetxtitle1')")
sql.execute(f"INSERT INTO works(username, title, forTeacher, course, predmet, isFree, grade, text) VALUES('username2', 'title2', 'forteacher2', 2, 'prednet2', True, 92, 'tttetxtitle2')")
sql.execute(f"INSERT INTO works(username, title, forTeacher, course, predmet, isFree, grade, text) VALUES('username3', 'title3', 'forteacher3', 3, 'prednet3', True, 93, 'tttetxtitle3')")
sql.execute(f"INSERT INTO works(username, title, forTeacher, course, predmet, isFree, grade, text) VALUES('username4', 'title4', 'forteacher4', 4, 'prednet4',False, 94, 'tttetxtitle4')")
sql.execute(f"INSERT INTO works(username, title, forTeacher, course, predmet, isFree, grade, text) VALUES('username5', 'title5', 'forteacher5', 5, 'prednet5', True, 94, 'tttetxtitle5')")
db.commit()

sql.execute('SELECT * FROM works')
data = []
for i in sql.fetchall():
    data_json = {}
    data_json['username'] = i[0]
    data_json['title'] = i[1]
    data_json['forTeacher'] = i[2]
    data_json['course'] = i[3]
    data_json['predmet'] = i[4]
    data_json['isFree'] = i[5]
    data_json['grade'] = i[6]
    data_json['text'] = i[7]
    data.append(data_json)

for i in data:
    print(i)

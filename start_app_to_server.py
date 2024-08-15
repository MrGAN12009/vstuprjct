import sys
import json
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import *


db = sqlite3.connect('zametki.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS zam (
        id BIGINT,
        date BIGINT,
        time INT,
        name TEXT
    )""")
db.commit()


class Main_Window(QMainWindow, QScrollArea):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.layout = QVBoxLayout()
        self.scroll = QScrollArea()

        self.btnAdd = QPushButton('Добавить заметку')
        self.btnAdd.clicked.connect(self.Add)
        self.btnDelete = QPushButton("Delete")
        self.btnDelete.clicked.connect(self.delete)

        self.layout.addWidget(self.btnAdd)
        sql.execute(f"SELECT name FROM zam")
        for j in sql.fetchall():
            MainLayout = QVBoxLayout()
            name = str(j)
            self.listBtn = QPushButton(f"{name[2:-3]}")
            self.listBtn.clicked.connect(
                lambda ch, name = name: self.zapis(name)
            )
            MainLayout.addWidget(self.listBtn)
            self.layout.addLayout(MainLayout)

        self.layout.addWidget(self.btnDelete)

        container = QWidget()
        container.setLayout(self.layout)

        self.scroll.setWidget(container)

        self.setCentralWidget(self.scroll)

    def main(self):
        self.setWindowTitle("Заметки")
        self.layout = QVBoxLayout()
        self.scroll = QScrollArea()

        self.btnAdd = QPushButton('Добавить заметку')
        self.btnAdd.clicked.connect(self.Add)
        self.btnDelete = QPushButton("Delete")
        self.btnDelete.clicked.connect(self.delete)

        self.layout.addWidget(self.btnAdd)
        sql.execute(f"SELECT name FROM zam")
        for j in sql.fetchall():
            MainLayout = QVBoxLayout()
            name = str(j)
            self.listBtn = QPushButton(f"{name[2:-3]}")
            self.listBtn.clicked.connect(
                lambda ch, name = name: self.zapis(name)
            )
            MainLayout.addWidget(self.listBtn)
            self.layout.addLayout(MainLayout)

        self.layout.addWidget(self.btnDelete)

        container = QWidget()
        container.setLayout(self.layout)

        self.scroll.setWidget(container)

        self.setCentralWidget(self.scroll)


    def zapis(self, name):

        add_layout = QVBoxLayout()

        self.name_z = QLabel(f"Title: {name[2:-3]}")
        a = json.load(open('file.json'))
        self.text_z = QLineEdit(f"{a.get(str(name[2:-3]))}")
        del a
        self.btnBack = QPushButton("Back")
        self.btnBack.clicked.connect(self.main)
        self.btnSafe = QPushButton("Safe")
        self.btnSafe.clicked.connect(
                lambda ch, name=name: self.reSafe(name)
            )


        add_layout.addWidget(self.btnBack)
        add_layout.addWidget(self.name_z)
        add_layout.addWidget(self.text_z)
        add_layout.addWidget(self.btnSafe)

        container = QWidget()
        container.setLayout(add_layout)
        self.setCentralWidget(container)

    def reSafe(self, name):
        a = json.load(open('file.json'))
        print('-')
        a[name[2:-3]] = f"{self.text_z.text().strip()}"
        print('--')
        json.dump(a, open('file.json', 'w'))

        self.main()


    def delete(self):
        self.setWindowTitle("Delete")
        self.layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.label = QLabel("Chose what delete")
        self.btnBack = QPushButton("Back")
        self.btnBack.clicked.connect(self.main)

        self.layout.addWidget(self.btnBack)
        self.layout.addWidget(self.label)
        sql.execute(f"SELECT name FROM zam")
        for j in sql.fetchall():
            MainLayout = QVBoxLayout()
            name = str(j)
            self.listBtn = QPushButton(f"{name[2:-3]}")
            self.listBtn.clicked.connect(
                lambda ch, name=name: self.deleteZapis(name)
            )
            MainLayout.addWidget(self.listBtn)
            self.layout.addLayout(MainLayout)

        container = QWidget()
        container.setLayout(self.layout)

        self.scroll.setWidget(container)

        self.setCentralWidget(self.scroll)


    def deleteZapis(self, name):
        print(name[2:-3])
        a = json.load(open('file.json'))
        try:
            a.pop(str(name[2:-3]))
        except BaseException:
            pass
        json.dump(a, open('file.json', 'w'))
        del a
        print('-')
        sql.execute(f"DELETE FROM zam WHERE name = '{name[2:-3]}'")
        db.commit()
        print('done')
        self.main()




    def Add(self):
        add_layout = QVBoxLayout()

        self.name = QLineEdit()
        self.text = QLineEdit()
        self.btnSafe = QPushButton('Сохранить')
        self.btnSafe.clicked.connect(self.safe)
        self.btnBack = QPushButton("Back")
        self.btnBack.clicked.connect(self.main)

        add_layout.addWidget(self.btnBack)
        add_layout.addWidget(self.name)
        add_layout.addWidget(self.text)
        add_layout.addWidget(self.btnSafe)

        container = QWidget()
        container.setLayout(add_layout)
        self.setCentralWidget(container)

    def safe(self):
        sql.execute("SELECT MAX(id) FROM zam")
        id1 = sql.fetchone()
        if "None" in str(id1):
            id = 0
        else:
            id = int(str(id1)[1:2])+1

        sql.execute("INSERT INTO zam (id, date, time, name) VALUES(?, ?, ?, ?)", (id, int((str(datetime.now()).split(" ")[0]).replace("-", "")), int((str(datetime.now()).split(" ")[1]).replace(":", "")[0:4]), self.name.text()))
        db.commit()

        try:
            a = json.load(open('file.json'))
        except BaseException:
            a = {}

        a.update({f"{self.name.text()}":f"{self.text.text().strip()}", })
        json.dump(a, open('file.json', 'w'))

        print("done")
        self.main()






app = QApplication(sys.argv)
window = Main_Window()
window.show()
app.exec()
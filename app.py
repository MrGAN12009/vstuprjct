import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import requests


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.label = QLabel('Введите номер человека:')
        self.le = QLineEdit()
        self.label2 = QLabel('Введите имя телефона:')
        self.name = QLineEdit()
        regex = QRegExp("^\\+?[1-9]\\d{1,14}$")
        validator = QRegExpValidator(regex)
        self.le.setValidator(validator)
        self.btn = QPushButton('Отправить', self)
        self.btn.clicked.connect(self.send_phone_number)
        self.btn1 = QPushButton('Все номера', self)
        self.btn1.clicked.connect(self.all_numbers)
        self.ans = QLabel('')

        vbox.addWidget(self.label2)
        vbox.addWidget(self.name)
        vbox.addWidget(self.label)
        vbox.addWidget(self.le)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.ans)

        self.setLayout(vbox)

        self.setWindowTitle('Отправка номера телефона')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def send_phone_number(self):
        phone_number = self.le.text().strip()
        name = self.name.text()

        flag = True

        if len(phone_number) == 11 and phone_number[0] == '8':
            print(1)
        elif len(phone_number) == 12 and phone_number[0:2] == '+7':
            print(2)
        else:
            self.label.setText("Неправильно введён номер.")
            flag == False





        if phone_number and name and flag == True:
            response = requests.post('http://192.168.0.163:8000', data={name: phone_number})
            print(response.status_code)

    def all_numbers(self):
        response = requests.get('http://192.168.0.163:8000')
        print(response.status_code)
        print(response.content)
        self.ans.setText(f"{response.content}")
        f = json.loads(response.content)
        with open('file.txt', 'w') as file:

            for i in f.keys():
                print(i, "=", f[i])
                file.write(f"{f[i]}  ---  {i}\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
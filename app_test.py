import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AuthWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Авторизация')
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        self.username_input.setObjectName("input")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("input")

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setObjectName("button")

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        # Здесь можно добавить проверку имени пользователя и пароля
        self.stacked_widget.setCurrentIndex(1)


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добро пожаловать')
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Привет, ты авторизован!', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")

        layout.addWidget(self.label)

        self.setLayout(layout)


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.auth_window = AuthWindow(self)
        self.welcome_window = WelcomeWindow()

        self.addWidget(self.auth_window)
        self.addWidget(self.welcome_window)

        self.setFixedSize(300, 200)
        self.setStyleSheet(self.load_stylesheet())

    def load_stylesheet(self):
        return """
        QWidget {
            background-color: #1c1c1e;
            color: #ffffff;
            font-family: 'Arial';
            font-size: 14px;
        }
        QLineEdit#input {
            background-color: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 10px;
            padding: 5px;
            color: #ffffff;
        }
        QPushButton#button {
            background-color: #0a84ff;
            border: none;
            border-radius: 10px;
            color: #ffffff;
            padding: 10px;
        }
        QPushButton#button:hover {
            background-color: #005ecb;
        }
        QLabel#label {
            font-size: 18px;
            font-weight: bold;
        }
        """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QStackedWidget, QScrollArea, QFrame, QMainWindow
)
from PyQt5.QtGui import QPalette, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import Qt

username = ''
jwt_token = ''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Application')
        self.setFixedSize(400, 400)

        # Create the stacked widget for managing screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize screens
        self.login_form = LoginForm(self)
        self.register_form = RegisterForm(self)
        self.main_menu = MainMenu(self)
        self.all_works_window = None  # To manage dynamic creation of "All works" screen

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.login_form)
        self.stacked_widget.addWidget(self.register_form)
        self.stacked_widget.addWidget(self.main_menu)

        # Set the initial screen
        self.stacked_widget.setCurrentWidget(self.login_form)

    def switch_to_register(self):
        self.stacked_widget.setCurrentWidget(self.register_form)

    def switch_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_form)

    def switch_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_all_works(self):
        if self.all_works_window is None:
            self.all_works_window = AllWorksWindow(self)
            self.stacked_widget.addWidget(self.all_works_window)
        self.stacked_widget.setCurrentWidget(self.all_works_window)

    def go_back_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        if self.all_works_window is not None:
            self.stacked_widget.removeWidget(self.all_works_window)
            self.all_works_window.deleteLater()  # Ensures proper memory management
            self.all_works_window = None

class LoginForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.main_window.switch_to_register)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def handle_login(self):
        global username, jwt_token
        username = self.username_input.text()
        password = self.password_input.text()
        data = {'username': username, 'password': password}
        try:
            response = requests.post('http://192.168.0.163:8000/login', data=data)
            if response.status_code == 200:
                jwt_token = response.content.decode("utf-8")
                self.main_window.switch_to_main_menu()
            else:
                QMessageBox.warning(self, "Error", "Login failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class RegisterForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText('Unique Access Key')

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.handle_register)

        self.back_button = QPushButton('Back to Login', self)
        self.back_button.clicked.connect(self.main_window.switch_to_login)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.key_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        access_key = self.key_input.text()

        data = {'username': username, 'password': password, 'access_key': access_key}
        try:
            response = requests.post('http://192.168.0.163:8000/register', data=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Registration successful!")
                self.main_window.switch_to_login()
            else:
                QMessageBox.warning(self, "Error", "Registration failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        buttons = [
            ('Все работы', self.main_window.show_all_works),
            ('Выложенные мной работы', lambda: QMessageBox.information(self, "Info", "Not implemented yet")),
            ('Купленные работы', lambda: QMessageBox.information(self, "Info", "Not implemented yet")),
            ('Профиль', lambda: QMessageBox.information(self, "Info", "Not implemented yet")),
        ]

        for text, handler in buttons:
            button = QPushButton(text, self)
            button.clicked.connect(handler)
            layout.addWidget(button)

        self.setLayout(layout)

class AllWorksWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)

        layout.addWidget(self.scroll_area)

        back_button = QPushButton('Назад', self)
        back_button.clicked.connect(self.main_window.go_back_to_main_menu)
        layout.addWidget(back_button)

        self.setLayout(layout)
        self.load_work_buttons()

    def load_work_buttons(self):
        global username, jwt_token
        try:
            headers = {
                'Authorization': f'{jwt_token}',
                'username': username
            }
            response = requests.get('http://192.168.0.163:8000/free_works', headers=headers)
            if response.status_code == 200:
                works = response.json().get("data", [])
                for work in works:
                    button = QPushButton(work['title'], self)
                    button.clicked.connect(lambda _, w=work: self.show_work_details(w))
                    self.scroll_area_content_layout.addWidget(button)
            else:
                QMessageBox.warning(self, "Error", "Failed to load works.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def show_work_details(self, work):
        details_window = WorkDetailsWindow(work, self.main_window)
        self.main_window.stacked_widget.addWidget(details_window)
        self.main_window.stacked_widget.setCurrentWidget(details_window)

class WorkDetailsWindow(QWidget):
    def __init__(self, work, main_window):
        super().__init__()
        self.work = work
        self.main_window = main_window

        layout = QVBoxLayout()
        title_label = QLabel(self.work['title'], self)
        description_label = QLabel(self.work['text'], self)

        back_button = QPushButton('Назад', self)
        back_button.clicked.connect(self.go_back)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def go_back(self):
        self.main_window.stacked_widget.removeWidget(self)
        self.deleteLater()  # Ensures proper memory management
        self.main_window.show_all_works()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

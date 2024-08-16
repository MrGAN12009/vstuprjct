import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QStackedLayout, QScrollArea, QFrame
from PyQt5.QtGui import QPalette, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import Qt
username = ''
jwt_token = ''


class LoginRegisterWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login/Register')
        self.setFixedSize(400, 400)

        self.gradient_background()

        self.stacked_layout = QStackedLayout()

        self.login_form = self.create_login_form()
        self.register_form = self.create_register_form()
        self.main_menu = self.create_main_menu()
        self.all_works_window = None

        self.stacked_layout.addWidget(self.login_form)
        self.stacked_layout.addWidget(self.register_form)
        self.stacked_layout.addWidget(self.main_menu)

        self.setLayout(self.stacked_layout)

    def gradient_background(self):
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setColorAt(0, QColor(34, 34, 34))
        gradient.setColorAt(1, QColor(50, 50, 50))

        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(gradient))
        self.setPalette(palette)

    def get_input_style(self):
        return """
        QLineEdit {
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
            color: #FFF;
            background-color: #222;
        }
        QLineEdit:focus {
            border: 1px solid #007AFF;
        }
        """

    def get_button_style(self):
        return """
        QPushButton {
            border: none;
            border-radius: 10px;
            padding: 10px;
            background-color: #007AFF;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0051A8;
        }
        QPushButton:pressed {
            background-color: #003F7F;
        }
        """

    def create_login_form(self):
        login_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.login_username_input = QLineEdit(self)
        self.login_username_input.setPlaceholderText('Username')
        self.login_username_input.setStyleSheet(self.get_input_style())

        self.login_password_input = QLineEdit(self)
        self.login_password_input.setPlaceholderText('Password')
        self.login_password_input.setStyleSheet(self.get_input_style())
        self.login_password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.setStyleSheet(self.get_button_style())
        self.login_button.clicked.connect(self.handle_login)

        self.switch_to_register_button = QPushButton('Register', self)
        self.switch_to_register_button.setStyleSheet(self.get_button_style())
        self.switch_to_register_button.clicked.connect(self.show_register_form)

        layout.addWidget(self.login_username_input)
        layout.addWidget(self.login_password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.switch_to_register_button)

        login_widget.setLayout(layout)
        return login_widget

    def create_register_form(self):
        register_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.register_username_input = QLineEdit(self)
        self.register_username_input.setPlaceholderText('Username')
        self.register_username_input.setStyleSheet(self.get_input_style())

        self.register_password_input = QLineEdit(self)
        self.register_password_input.setPlaceholderText('Password')
        self.register_password_input.setStyleSheet(self.get_input_style())
        self.register_password_input.setEchoMode(QLineEdit.Password)

        self.register_key_input = QLineEdit(self)
        self.register_key_input.setPlaceholderText('Unique Access Key')
        self.register_key_input.setStyleSheet(self.get_input_style())

        self.register_button = QPushButton('Register', self)
        self.register_button.setStyleSheet(self.get_button_style())
        self.register_button.clicked.connect(self.handle_register)

        self.switch_to_login_button = QPushButton('Back to Login', self)
        self.switch_to_login_button.setStyleSheet(self.get_button_style())
        self.switch_to_login_button.clicked.connect(self.show_login_form)

        layout.addWidget(self.register_username_input)
        layout.addWidget(self.register_password_input)
        layout.addWidget(self.register_key_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.switch_to_login_button)

        register_widget.setLayout(layout)
        return register_widget

    def create_main_menu(self):
        main_menu = QWidget()
        layout = QVBoxLayout()

        buttons = [
            ('Все работы', self.show_all_works_window),
            ('Выложенные мной работы', lambda: self.show_work_window('Выложенные мной работы')),
            ('Купленные работы', lambda: self.show_work_window('Купленные работы')),
            ('Заказать работу', lambda: self.show_work_window('Заказать работу')),
            ('Заказы на работу', lambda: self.show_work_window('Заказы на работу')),
        ]

        for text, handler in buttons:
            button = QPushButton(text)
            button.setStyleSheet(self.get_button_style())
            button.clicked.connect(handler)
            layout.addWidget(button)

        main_menu.setLayout(layout)
        return main_menu

    def handle_login(self):
        global username, jwt_token
        username = self.login_username_input.text()
        password = self.login_password_input.text()
        data = {'username': username, 'password': password}
        try:
            response = requests.post('http://192.168.0.163:8000/login', data=data)
            if response.status_code == 200:
                jwt_token = jwt_token = response.content.decode("utf-8")
                self.stacked_layout.setCurrentWidget(self.main_menu)
            else:
                QMessageBox.warning(self, "Error", "Login failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def handle_register(self):
        username = self.register_username_input.text()
        password = self.register_password_input.text()
        access_key = self.register_key_input.text()

        data = {'username': username, 'password': password, 'access_key': access_key}
        try:
            response = requests.post('http://192.168.0.163:8000/register', data=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Registration successful!")
                self.show_login_form()
            else:
                QMessageBox.warning(self, "Error", "Registration failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def show_login_form(self):
        self.stacked_layout.setCurrentWidget(self.login_form)

    def show_register_form(self):
        self.stacked_layout.setCurrentWidget(self.register_form)

    def show_all_works_window(self):
        if self.all_works_window is None:
            self.all_works_window = AllWorksWindow(self.stacked_layout, self.main_menu)
            self.stacked_layout.addWidget(self.all_works_window)
        self.stacked_layout.setCurrentWidget(self.all_works_window)

    def show_work_window(self, title):
        self.work_window = WorkWindow(title, self.stacked_layout, self.main_menu)
        self.stacked_layout.addWidget(self.work_window)
        self.stacked_layout.setCurrentWidget(self.work_window)


class AllWorksWindow(QWidget):
    def __init__(self, stacked_layout, main_menu):
        super().__init__()
        self.setWindowTitle('Все работы')
        self.setFixedSize(400, 400)
        self.stacked_layout = stacked_layout
        self.main_menu = main_menu
        self.gradient_background()

        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content_layout = QVBoxLayout()
        self.scroll_area_content.setLayout(self.scroll_area_content_layout)
        self.scroll_area.setWidget(self.scroll_area_content)

        layout.addWidget(self.scroll_area)

        back_button = QPushButton('Назад')
        back_button.setStyleSheet(self.get_button_style())
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)
        self.load_work_buttons()

    def gradient_background(self):
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setColorAt(0, QColor(34, 34, 34))
        gradient.setColorAt(1, QColor(50, 50, 50))

        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(gradient))
        self.setPalette(palette)

    def get_button_style(self):
        return """
        QPushButton {
            border: none;
            border-radius: 10px;
            padding: 10px;
            background-color: #007AFF;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0051A8;
        }
        QPushButton:pressed {
            background-color: #003F7F;
        }
        """

    def load_work_buttons(self):
        global username, jwt_token
        try:
            headers = {
                'Authorization': jwt_token,
                'username': username}
            response = requests.get('http://192.168.0.163:8000/free_works', headers=headers)
            if response.status_code == 200:
                data = response.json()
                works = data.get("data", [])
                print(works)
                for work in works:
                    button = QPushButton(work['title'])
                    button.setStyleSheet(self.get_button_style())
                    button.clicked.connect(lambda _, w=work: self.show_work_details(w))
                    self.scroll_area_content_layout.addWidget(button)
            else:
                QMessageBox.warning(self, "Error", "Failed to load works.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def show_work_details(self, work):
        work_details_window = WorkDetailsWindow(work, self.stacked_layout, self)
        self.stacked_layout.addWidget(work_details_window)
        self.stacked_layout.setCurrentWidget(work_details_window)

    def go_back(self):
        self.stacked_layout.setCurrentWidget(self.main_menu)
        self.stacked_layout.removeWidget(self)


class WorkDetailsWindow(QWidget):
    def __init__(self, work, stacked_layout, parent_window):
        super().__init__()
        self.setWindowTitle('Work Details')
        self.setFixedSize(400, 400)
        self.work = work
        self.stacked_layout = stacked_layout
        self.parent_window = parent_window
        self.gradient_background()

        layout = QVBoxLayout()

        title_label = QLabel(self.work['title'])
        title_label.setStyleSheet("color: white; font-size: 18px;")
        title_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(self.work['description'])
        description_label.setStyleSheet("color: white; font-size: 14px;")
        description_label.setAlignment(Qt.AlignCenter)

        back_button = QPushButton('Назад')
        back_button.setStyleSheet(self.get_button_style())
        back_button.clicked.connect(self.go_back)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def gradient_background(self):
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setColorAt(0, QColor(34, 34, 34))
        gradient.setColorAt(1, QColor(50, 50, 50))

        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(gradient))
        self.setPalette(palette)

    def get_button_style(self):
        return """
        QPushButton {
            border: none;
            border-radius: 10px;
            padding: 10px;
            background-color: #007AFF;
            color: white;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0051A8;
        }
        QPushButton:pressed {
            background-color: #003F7F;
        }
        """

    def go_back(self):
        self.stacked_layout.setCurrentWidget(self.parent_window)
        self.stacked_layout.removeWidget(self)


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

    window = LoginRegisterWindow()
    window.show()
    sys.exit(app.exec_())

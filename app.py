import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QStackedWidget, QScrollArea, QMainWindow, QComboBox, QCheckBox
)
from PyQt5.QtGui import QPalette, QColor, QBrush, QLinearGradient, QPainter, QIntValidator
from PyQt5.QtCore import Qt

username = ''
jwt_token = ''

class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(25, 25, 25))
        gradient.setColorAt(1, QColor(53, 53, 53))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(self.palette().window())
        painter.drawRect(self.rect())

class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #424242;
                border: 2px solid #616161;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #616161;
            }
        """)

class RoundedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #616161;
                border-radius: 10px;
                padding: 10px;
                background-color: #333;
                color: white;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Application')
        self.setFixedSize(400, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_form = LoginForm(self)
        self.register_form = RegisterForm(self)
        self.main_menu = MainMenu(self)
        self.add_work_window = None
        self.all_works_window = None

        self.stacked_widget.addWidget(self.login_form)
        self.stacked_widget.addWidget(self.register_form)
        self.stacked_widget.addWidget(self.main_menu)

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

    def show_add_work(self):
        if self.add_work_window is None:
            self.add_work_window = AddWorkWindow(self)
            self.stacked_widget.addWidget(self.add_work_window)
        self.stacked_widget.setCurrentWidget(self.add_work_window)

    def go_back_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        if self.all_works_window is not None:
            self.stacked_widget.removeWidget(self.all_works_window)
            self.all_works_window.deleteLater()
            self.all_works_window = None
        if self.add_work_window is not None:
            self.stacked_widget.removeWidget(self.add_work_window)
            self.add_work_window.deleteLater()
            self.add_work_window = None

class LoginForm(GradientWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        self.username_input = RoundedLineEdit(self)
        self.username_input.setPlaceholderText('Username')

        self.password_input = RoundedLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = RoundedButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = RoundedButton('Register', self)
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
            response = requests.post('http://185.180.109.43:8000/login', json=data)
            if response.status_code == 200:
                jwt_token = response.content.decode("utf-8")
                self.main_window.switch_to_main_menu()
            else:
                QMessageBox.warning(self, "Error", "Login failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class RegisterForm(GradientWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        self.username_input = RoundedLineEdit(self)
        self.username_input.setPlaceholderText('Username')

        self.password_input = RoundedLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.key_input = RoundedLineEdit(self)
        self.key_input.setPlaceholderText('Unique Access Key')

        self.register_button = RoundedButton('Register', self)
        self.register_button.clicked.connect(self.handle_register)

        self.back_button = RoundedButton('Back to Login', self)
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
            response = requests.post('http://185.180.109.43:8000/register', json=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Registration successful!")
                self.main_window.switch_to_login()
            else:
                QMessageBox.warning(self, "Error", "Registration failed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class MainMenu(GradientWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        buttons = [
            ('Все работы', self.main_window.show_all_works),
            ('Добавить работу', self.main_window.show_add_work),
            ('Выложенные мной работы', lambda: QMessageBox.information(self, "Info", "Not implemented yet")),
            ('Купленные работы', lambda: QMessageBox.information(self, "Info", "Not implemented yet")),
            ('Профиль', lambda: QMessageBox.information(self, "Info", "Not implemented yet")),
        ]

        for text, handler in buttons:
            button = RoundedButton(text, self)
            button.clicked.connect(handler)
            layout.addWidget(button)

        self.setLayout(layout)

class AllWorksWindow(GradientWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.teachers = ['Teacher 1', 'Teacher 2', 'Teacher 3']
        self.predmets = ['Subject 1', 'Subject 2', 'Subject 3']

        layout = QVBoxLayout()

        # Фильтры
        self.teacher_input = QComboBox(self)
        self.teacher_input.addItems(self.teachers)
        self.teacher_input.setEditable(True)

        self.course_input = RoundedLineEdit(self)
        self.course_input.setPlaceholderText('Course')
        self.course_input.setValidator(QIntValidator())

        self.predmet_input = QComboBox(self)
        self.predmet_input.addItems(self.predmets)
        self.predmet_input.setEditable(True)

        self.is_free_checkbox = QCheckBox('Free', self)

        self.grade_input = RoundedLineEdit(self)
        self.grade_input.setPlaceholderText('Grade')
        self.grade_input.setValidator(QIntValidator())

        self.apply_filters_button = RoundedButton('Apply Filters', self)
        self.apply_filters_button.clicked.connect(self.load_work_buttons)

        filter_layout = QVBoxLayout()
        filter_layout.addWidget(QLabel('Teacher:', self))
        filter_layout.addWidget(self.teacher_input)
        filter_layout.addWidget(QLabel('Course:', self))
        filter_layout.addWidget(self.course_input)
        filter_layout.addWidget(QLabel('Subject:', self))
        filter_layout.addWidget(self.predmet_input)
        filter_layout.addWidget(QLabel('Free:', self))
        filter_layout.addWidget(self.is_free_checkbox)
        filter_layout.addWidget(QLabel('Grade:', self))
        filter_layout.addWidget(self.grade_input)
        filter_layout.addWidget(self.apply_filters_button)

        layout.addLayout(filter_layout)

        # Прокручиваемая область
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)

        layout.addWidget(self.scroll_area)

        back_button = RoundedButton('Назад', self)
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
            response = requests.get('http://185.180.109.43:8000/free_works', headers=headers)
            if response.status_code == 200:
                works = response.json().get("data", [])
                for work in works:
                    button = RoundedButton(work['title'], self)
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

class WorkDetailsWindow(GradientWidget):
    def __init__(self, work, main_window):
        super().__init__()
        self.work = work
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Username: {self.work['username']}", self))
        layout.addWidget(QLabel(f"Title: {self.work['title']}", self))
        layout.addWidget(QLabel(f"For Teacher: {self.work['forTeacher']}", self))
        layout.addWidget(QLabel(f"Course: {self.work['course']}", self))
        layout.addWidget(QLabel(f"Subject: {self.work['predmet']}", self))
        layout.addWidget(QLabel(f"Grade: {self.work['grade']}", self))
        layout.addWidget(QLabel(f"Text: {self.work['text']}", self))

        back_button = RoundedButton('Назад', self)
        back_button.clicked.connect(self.go_back)

        layout.addWidget(back_button)
        self.setLayout(layout)

    def go_back(self):
        self.main_window.stacked_widget.removeWidget(self)
        self.deleteLater()  # Ensures proper memory management
        self.main_window.show_all_works()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

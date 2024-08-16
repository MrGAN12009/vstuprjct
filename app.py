import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QStackedWidget, QScrollArea, QMainWindow
)
from PyQt5.QtGui import QPalette, QColor, QBrush, QLinearGradient, QPainterPath, QPainter
from PyQt5.QtCore import Qt, QRectF

username = ''
jwt_token = ''

class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setPalette(QPalette(QColor(53, 53, 53)))
        self.gradient = QLinearGradient(0, 0, 0, self.height())
        self.gradient.setColorAt(0, QColor(25, 25, 25))
        self.gradient.setColorAt(1, QColor(53, 53, 53))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.gradient))
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

        # Create the stacked widget for managing screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize screens
        self.login_form = LoginForm(self)
        self.register_form = RegisterForm(self)
        self.main_menu = MainMenu(self)
        self.add_work_window = None  # To manage dynamic creation of "Add Work" screen
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

    def show_add_work(self):
        if self.add_work_window is None:
            self.add_work_window = AddWorkWindow(self)
            self.stacked_widget.addWidget(self.add_work_window)
        self.stacked_widget.setCurrentWidget(self.add_work_window)

    def go_back_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        if self.all_works_window is not None:
            self.stacked_widget.removeWidget(self.all_works_window)
            self.all_works_window.deleteLater()  # Ensures proper memory management
            self.all_works_window = None
        if self.add_work_window is not None:
            self.stacked_widget.removeWidget(self.add_work_window)
            self.add_work_window.deleteLater()  # Ensures proper memory management
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

        layout = QVBoxLayout()

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
        title_label = QLabel(self.work['title'], self)
        description_label = QLabel(self.work['text'], self)

        back_button = RoundedButton('Назад', self)
        back_button.clicked.connect(self.go_back)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def go_back(self):
        self.main_window.stacked_widget.removeWidget(self)
        self.deleteLater()  # Ensures proper memory management
        self.main_window.show_all_works()

class AddWorkWindow(GradientWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()

        # Поля для ввода данных
        self.title_input = RoundedLineEdit(self)
        self.title_input.setPlaceholderText('Title (макс. 45 символов)')
        self.title_input.setMaxLength(45)

        self.for_teacher_input = RoundedLineEdit(self)
        self.for_teacher_input.setPlaceholderText('For Teacher (макс. 45 символов)')
        self.for_teacher_input.setMaxLength(45)

        self.course_input = RoundedLineEdit(self)
        self.course_input.setPlaceholderText('Course (число)')

        self.predmet_input = RoundedLineEdit(self)
        self.predmet_input.setPlaceholderText('Predmet (макс. 45 символов)')
        self.predmet_input.setMaxLength(45)

        self.grade_input = RoundedLineEdit(self)
        self.grade_input.setPlaceholderText('Grade (число)')

        self.is_free_checkbox = RoundedButton('Is Free (Нажмите, если бесплатно)', self)
        self.is_free_checkbox.setCheckable(True)

        self.text_input = RoundedLineEdit(self)
        self.text_input.setPlaceholderText('Text (макс. 500 символов)')
        self.text_input.setMaxLength(500)

        # Кнопка для отправки данных
        self.submit_button = RoundedButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_work)

        # Кнопка для возврата назад
        self.back_button = RoundedButton('Назад', self)
        self.back_button.clicked.connect(self.main_window.go_back_to_main_menu)

        # Добавление всех элементов на макет
        layout.addWidget(self.title_input)
        layout.addWidget(self.for_teacher_input)
        layout.addWidget(self.course_input)
        layout.addWidget(self.predmet_input)
        layout.addWidget(self.grade_input)
        layout.addWidget(self.is_free_checkbox)
        layout.addWidget(self.text_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def submit_work(self):
        title = self.title_input.text()
        for_teacher = self.for_teacher_input.text()
        course = self.course_input.text()
        predmet = self.predmet_input.text()
        grade = self.grade_input.text()
        is_free = self.is_free_checkbox.isChecked()
        text = self.text_input.text()

        data = {
            'username': username,
            'title': title,
            'forTeacher': for_teacher,
            'course': int(course) if course.isdigit() else 1,
            'predmet': predmet,
            'isFree': is_free,
            'grade': int(grade) if grade.isdigit() else 1,
            'text': text
        }

        try:
            headers = {'Authorization': f'{jwt_token}', 'username': username}
            response = requests.post('http://185.180.109.43:8000/new_work', json=data, headers=headers)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Work added successfully!")
                self.main_window.go_back_to_main_menu()
            else:
                QMessageBox.warning(self, "Error", "Failed to add work.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

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

import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

# Настройка глобальных переменных
username = ''
jwt_token = ''


# Основное окно приложения
class MainWindow(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_screen = LoginScreen(name='login')
        self.register_screen = RegisterScreen(name='register')
        self.main_menu_screen = MainMenuScreen(name='main_menu')
        self.all_works_screen = AllWorksScreen(name='all_works')

        self.add_widget(self.login_screen)
        self.add_widget(self.register_screen)
        self.add_widget(self.main_menu_screen)
        self.add_widget(self.all_works_screen)


# Экран входа
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.username_input = TextInput(hint_text="Username", size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40)

        login_button = Button(text="Login", size_hint_y=None, height=50)
        login_button.bind(on_release=self.handle_login)

        register_button = Button(text="Register", size_hint_y=None, height=50)
        register_button.bind(on_release=self.switch_to_register)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def handle_login(self, instance):
        global username, jwt_token
        username = self.username_input.text
        password = self.password_input.text
        data = {'username': username, 'password': password}
        try:
            response = requests.post('http://185.180.109.43:8000/login', data=data)
            if response.status_code == 200:
                jwt_token = response.content.decode("utf-8")
                self.manager.current = 'main_menu'
            else:
                self.show_error("Login failed.")
        except Exception as e:
            self.show_error(f"An error occurred: {e}")

    def switch_to_register(self, instance):
        self.manager.current = 'register'

    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()


# Экран регистрации
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.username_input = TextInput(hint_text="Username", size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text="Password", password=True, size_hint_y=None, height=40)
        self.key_input = TextInput(hint_text="Unique Access Key", size_hint_y=None, height=40)

        register_button = Button(text="Register", size_hint_y=None, height=50)
        register_button.bind(on_release=self.handle_register)

        back_button = Button(text="Back to Login", size_hint_y=None, height=50)
        back_button.bind(on_release=self.switch_to_login)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.key_input)
        layout.add_widget(register_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def handle_register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        access_key = self.key_input.text

        data = {'username': username, 'password': password, 'access_key': access_key}
        try:
            response = requests.post('http://185.180.109.43:8000/register', data=data)
            if response.status_code == 200:
                self.show_success("Registration successful!")
                self.manager.current = 'login'
            else:
                self.show_error("Registration failed.")
        except Exception as e:
            self.show_error(f"An error occurred: {e}")

    def switch_to_login(self, instance):
        self.manager.current = 'login'

    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()

    def show_success(self, message):
        popup = Popup(title='Success', content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()


# Главное меню
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        all_works_button = Button(text="Все работы", size_hint_y=None, height=50)
        all_works_button.bind(on_release=self.switch_to_all_works)

        my_works_button = Button(text="Выложенные мной работы", size_hint_y=None, height=50)
        purchased_works_button = Button(text="Купленные работы", size_hint_y=None, height=50)
        profile_button = Button(text="Профиль", size_hint_y=None, height=50)

        layout.add_widget(all_works_button)
        layout.add_widget(my_works_button)
        layout.add_widget(purchased_works_button)
        layout.add_widget(profile_button)

        self.add_widget(layout)

    def switch_to_all_works(self, instance):
        self.manager.current = 'all_works'


# Экран "Все работы"
class AllWorksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100))
        self.grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        self.scroll_view.add_widget(self.grid_layout)

        layout.add_widget(self.scroll_view)

        back_button = Button(text="Назад", size_hint_y=None, height=50)
        back_button.bind(on_release=self.go_back_to_main_menu)

        layout.add_widget(back_button)

        self.add_widget(layout)
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
                    button = Button(text=work['title'], size_hint_y=None, height=50)
                    button.bind(on_release=lambda btn, w=work: self.show_work_details(w))
                    self.grid_layout.add_widget(button)
            else:
                self.show_error("Failed to load works.")
        except Exception as e:
            self.show_error(f"An error occurred: {e}")

    def show_work_details(self, work):
        details_screen = WorkDetailsScreen(work, name='work_details')
        self.manager.add_widget(details_screen)
        self.manager.current = 'work_details'

    def go_back_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()


# Экран деталей работы
class WorkDetailsScreen(Screen):
    def __init__(self, work, **kwargs):
        super().__init__(**kwargs)
        self.work = work

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        title_label = Label(text=self.work['title'], font_size='20sp')
        description_label = Label(text=self.work['text'], size_hint_y=None, height=300)

        back_button = Button(text="Назад", size_hint_y=None, height=50)
        back_button.bind(on_release=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(description_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.remove_widget(self)
        self.manager.current = 'all_works'


# Основной класс приложения
class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Белый фон, в стиле минимализма Apple
        return MainWindow()


if __name__ == '__main__':
    MyApp().run()

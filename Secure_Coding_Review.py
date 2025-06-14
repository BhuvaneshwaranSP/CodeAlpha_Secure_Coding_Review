from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import json
import os

Window.clearcolor = get_color_from_hex("#F2F2F2")

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def find_user(username, password=None):
    users = load_users()
    for user in users:
        if user['username'] == username and (password is None or user['password'] == password):
            return True
    return False

def register_user(username, password):
    users = load_users()
    if find_user(username):
        return False, "User already exists"
    users.append({'username': username, 'password': password})
    save_users(users)
    return True, "Registered successfully"

def list_users():
    users = load_users()
    if not users:
        return "No users found."
    return "\n".join([f"- {u['username']}" for u in users])

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        layout = BoxLayout(orientation='vertical', spacing=15, padding=30, size_hint=(.9, .7))

        self.username = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=50)
        self.password = TextInput(hint_text="Password", multiline=False, password=True, size_hint_y=None, height=50)

        for field in [self.username, self.password]:
            field.font_size = 18
            field.background_color = get_color_from_hex("#FFFFFF")
            field.foreground_color = get_color_from_hex("#000000")
            field.padding = [15, 15]

        btn_register = Button(text="Register", size_hint_y=None, height=50, background_color=get_color_from_hex("#4CAF50"))
        btn_login = Button(text="Login", size_hint_y=None, height=50, background_color=get_color_from_hex("#2196F3"))
        btn_users = Button(text="Show Users", size_hint_y=None, height=50, background_color=get_color_from_hex("#9C27B0"))

        for btn in [btn_register, btn_login, btn_users]:
            btn.color = (1, 1, 1, 1)
            btn.font_size = 16

        btn_register.bind(on_press=self.do_register)
        btn_login.bind(on_press=self.do_login)
        btn_users.bind(on_press=self.show_users)

        layout.add_widget(Label(text="Secure App", font_size=26, size_hint_y=None, height=50, color=(0, 0.5, 0.5, 1)))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(btn_register)
        layout.add_widget(btn_login)
        layout.add_widget(btn_users)

        anchor.add_widget(layout)
        self.add_widget(anchor)

    def navigate(self, result):
        self.manager.current = "result"
        self.manager.get_screen("result").update_result(result)

    def do_register(self, _):
        success, message = register_user(self.username.text.strip(), self.password.text.strip())
        self.navigate(message)

    def do_login(self, _):
        if find_user(self.username.text.strip(), self.password.text.strip()):
            self.navigate("Login successful.")
        else:
            self.navigate("Login failed.")

    def show_users(self, _):
        self.navigate(list_users())

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = Label(
            text="",
            font_size=18,
            halign="left",
            valign="top",
            color=(0, 0, 0, 1)
        )
        self.label.bind(size=self.label.setter('text_size'))

        btn_back = Button(
            text="Back",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex("#607D8B"),
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))

        layout.add_widget(self.label)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def update_result(self, result_text):
        self.label.text = result_text

class SecureApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == "__main__":
    SecureApp().run()

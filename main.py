from kivy.app import App
from screens.login import Login
from screens.register import Register
from screens.home import Home
from screens.view import View
from screens.edit import Edit
from screens.monthly import Monthly
from kivy.uix.screenmanager import ScreenManager

class ManageWindows(ScreenManager):
    pass

class FinanceTrackerApp(App):
    def build(self):
        sm = ManageWindows()
        sm.add_widget(Login(name="login"))
        sm.add_widget(Register(name="register"))
        sm.add_widget(Home(name="home"))
        sm.add_widget(View(name="view"))
        sm.add_widget(Edit(name="edit"))
        sm.add_widget(Monthly(name="monthly"))
        return sm

if __name__ == "__main__":
    FinanceTrackerApp().run()

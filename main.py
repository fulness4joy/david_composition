from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        logo = Image(source = 'assets/images/logo.png', fit_mode='fill')
        button1 = Button(text = "открыть", font_size = "40sp")
        label1 = Label(text = "Склад", font_size = "40sp")

        box = BoxLayout(orientation = "vertical")
        box.add_widget(label1)
        box.add_widget(logo)
        box.add_widget(button1)
        self.add_widget(box)

        button1.on_press = self.goto_main

    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "down"


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        logo = Image(source = 'assets/images/logo.png', fit_mode='fill')
        button1 = Button(text = "открыть", size_hint = (0.7, 1))
        button2 = Button(text = "закрыть", size_hint = (0.3, 1))


        box = BoxLayout(orientation = "horizontal")
        # box.add_widget(logo)
        box.add_widget(button1)
        box.add_widget(button2)

        self.add_widget(box)
        


class CompositionApp(App):
    def build(self):
        scr_sm = ScreenManager()
        scr_sm.add_widget(MenuScreen(name = "menu"))
        scr_sm.add_widget(MainScreen(name = "main"))


        return scr_sm


if __name__ == '__main__':
    app = CompositionApp()
    app.run()
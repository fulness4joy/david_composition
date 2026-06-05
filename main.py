from settings import*
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window 

    

class BoxRow(BoxLayout):
    ...    


class MenuScreen(Screen):
    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "down"


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    def on_kv_post(self, base_widget):

        self.ids.main_container.add_widget(BoxRow())

        return super().on_kv_post(base_widget)
     
    def goto_main(self):
        self.manager.current = "menu"
        self.manager.transition.direction = "up"
        

class CompositionApp(App):
    def build(self):
        scr_sm = ScreenManager()
        scr_sm.add_widget(MenuScreen(name = "menu"))
        scr_sm.add_widget(MainScreen(name = "main"))


        return scr_sm


if __name__ == '__main__':

    Window.clearcolor = (0.12, 0.16, 0.22, 1)
    Window.size = (450, 900)

    app = CompositionApp()
    app.run()
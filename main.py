import os
from settings import*
from resources import*
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.core.window import Window 


class BoxRow(BoxLayout):
    pass  


class MainLabel(Label):
    pass


class MenuScreen(Screen):
    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "down"


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.load_products()

    def on_kv_post(self, base_widget):
        self.ids.main_container.add_widget(BoxRow())

        return super().on_kv_post(base_widget)

    def load_products(self):
        with open(PATH, "r", encoding = "utf8") as file:    
            lines = file.readlines()
        gl = GridLayout(orientation = 'lr-tb', cols = 1, padding = '20dp', spacing = '10dp')
        
        for e in lines:
            space = e.find(" ")
            product = e[0:space]
            weight = e[space + 1:-1]
            
            bl = BoxLayout(size_hint_y = None, height = dp(50), spacing = '10dp')
            bl.add_widget(MainLabel(text = product))
            bl.add_widget(MainLabel(text = weight))
            bl.add_widget(Image(source = RESOURCES[product]))
            gl.add_widget(bl)

        self.ids.main_container.add_widget(gl)
            
    def goto_main(self):
        self.manager.current = "menu"
        self.manager.transition.direction = "up"
        

class CompositionApp(App):
    resources = RESOURCES
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
from settings import*
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window 
Window.clearcolor = (1, 1, 1, 1)


class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        logo = Image(source = 'assets/images/logo.png', fit_mode='fill')
        button1 = Button(text = "открыть", font_size = "40sp", font_name = "assets/CascadiaCode.ttf")
        label1 = Label(text = "Склад", font_size = "40sp", color = "black", font_name = "assets/CascadiaCode.ttf")

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
        banana = Image(source = 'assets/images/banana.png', size_hint = (0.1, 0.1))  
        strawberry = Image(source = 'assets/images/strawberry.png', size_hint = (0.1, 0.1))  
        watermelon = Image(source = 'assets/images/watermelon.png', size_hint = (0.1, 0.1))  
        pineapple = Image(source = 'assets/images/pineapple.png', size_hint = (0.1, 0.1))  
        apple = Image(source = 'assets/images/apple.png', size_hint = (0.1, 0.1))  
        grepes = Image(source = 'assets/images/grepes.png', size_hint = (0.1, 0.1))  
        label_bnn = Label(text = "Банан         14кг", color = "black", font_name = "assets/CascadiaCode.ttf")
        label_sbr = Label(text = "Клубника      6кг", color = "black", font_name = "assets/CascadiaCode.ttf")
        label_wmn = Label(text = "Арбуз         10кг", color = "black", font_name = "assets/CascadiaCode.ttf")
        label_pal = Label(text = "Ананас        7кг", color = "black", font_name = "assets/CascadiaCode.ttf")
        label_apl = Label(text = "Яблоки        15кг", color = "black", font_name = "assets/CascadiaCode.ttf")
        label_gps = Label(text = "Винорад       8кг", color = "black", font_name = "assets/CascadiaCode.ttf")

        box = BoxLayout(orientation = "vertical") 
        box2 = BoxLayout(orientation = "vertical") 
        box.add_widget(banana)
        box.add_widget(strawberry)
        box.add_widget(watermelon)
        box.add_widget(pineapple)
        box.add_widget(apple)
        box.add_widget(grepes)
        box2.add_widget(label_bnn)
        box2.add_widget(label_sbr)
        box2.add_widget(label_wmn)
        box2.add_widget(label_pal)
        box2.add_widget(label_apl)
        box2.add_widget(label_gps)

        self.add_widget(box)
        self.add_widget(box2)


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
    app = CompositionApp()
    app.run()
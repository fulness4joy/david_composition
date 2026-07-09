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
from kivy.properties import StringProperty



class BoxRow(BoxLayout):
    product_name = StringProperty("")

    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and self.product_name:
            app = App.get_running_app()
            product_screen = app.root.get_screen('product_screen')
            product_screen.load_product(self.product_name)
            app.root.current = 'product_screen'
        return super().on_touch_up(touch) 
        

class MainLabel(Label):
    pass


class MainImage(Image):
    pass


class ProductScreen(Screen):
    product_name = StringProperty("")
    product_image = StringProperty("")
    product_quantity = StringProperty("0")

    def __init__(self, **kw):
        super().__init__(**kw)

    def read_products(self):
        with open(PATH_DATA + "list_products.txt", "r", encoding="utf8") as file:
            lines = file.readlines()

        products = []
        for e in lines:
            e = e.strip()
            if not e:
                continue
            space = e.find(" ")
            name = e[0:space]
            weight = e[space + 1:]
            products.append((name, weight))
        return products
    
    def write_products(self, products):
        with open(PATH_DATA + "list_products.txt", "w", encoding="utf8") as file:
            for name, weight in products:
                file.write(f"{name} {weight}\n")

    def load_product(self, name):
        self.product_name = name
        self.product_image = RESOURCES[name]
        self.product_quantity = "0"
        for prod_name, weight in self.read_products():
            if prod_name == name:
                self.product_quantity = weight
                break

    def save_quantity(self):
        products = self.read_products()
        new_products = []

        for name, weight in products:
            if name == self.product_name:
                new_products.append((name, self.product_quantity))
            else:
                new_products.append((name, weight))

        products = new_products
        self.write_products(products)

    def add_quantity(self):
        quantity = int(self.product_quantity)
        quantity += 1

        self.product_quantity = str(quantity)
        self.save_quantity()

    def delete_quantity(self):
        quantity = int(self.product_quantity)
        if quantity >= 1: 
            quantity -= 1

            self.product_quantity = str(quantity)
            self.save_quantity()

    def delete_product(self):
        products = self.read_products()
        new_products = []

        for name, weight in products:
            if name != self.product_name:
                new_products.append((name, weight))

        self.write_products(new_products)

        self.goto_main()

    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "down"


class MenuScreen(Screen):
    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "down"


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.load_resources()

    def load_resources(self):
        with open(PATH_DATA + "list_resources.txt", "r", encoding = "utf8") as file:    
            lines = file.readlines()
        
        for e in lines:
            e = e.strip()
            if not e:
                continue
            space = e.find(" ")
            key = e[0:space]
            path = e[space + 1:]
            RESOURCES[key] = path

    def load_products(self):
        screen = self.manager.get_screen("product_screen")
        self.ids.main_container.clear_widgets()

        for product, weight in screen.read_products():
            bl = BoxRow(size_hint_y = None, height = dp(50), spacing = '10dp', product_name = product)
            bl.add_widget(MainLabel(text = product))
            bl.add_widget(MainLabel(text = weight))
            bl.add_widget(MainImage(source = RESOURCES[product]))

            self.ids.main_container.add_widget(bl)

    def reload_products(self):
        self.load_products()

    def on_pre_enter(self, *args):
        self.load_products()
        return super().on_pre_enter(*args)

    def goto_main(self):
        self.manager.current = "menu"
        self.manager.transition.direction = "up"
        

class CompositionApp(App):
    resources = RESOURCES
    def build(self):
        scr_sm = ScreenManager()
        scr_sm.add_widget(MenuScreen(name = "menu"))
        scr_sm.add_widget(MainScreen(name = "main"))
        scr_sm.add_widget(ProductScreen(name = "product_screen"))


        return scr_sm


if __name__ == '__main__':

    Window.clearcolor = (0.12, 0.16, 0.22, 1)
    Window.size = (450, 900)

    app = CompositionApp()
    app.run()
import os
import json
from settings import *
from resources import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.checkbox import CheckBox


def get_box_count(name):
    for item in basket_quantity:
        if item[0] == name:
            return item[1]
    return 0


def set_box_count(name, count):
    for item in basket_quantity:
        if item[0] == name:
            item[1] = count
            return
    basket_quantity.append([name, count])


def remove_box_count(name):
    for item in basket_quantity:
        if item[0] == name:
            basket_quantity.remove(item)
            return


class BoxRow(BoxLayout):
    product_name = StringProperty("")
    product_price = StringProperty("")
    product_volume = StringProperty("")
    product_quantity = StringProperty("")
    cb_active = BooleanProperty(False)

    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and self.product_name:
            app = App.get_running_app()
            product_screen = app.root.get_screen("product_screen")
            product_screen.load_product(self.product_name)
            app.root.current = "product_screen"
        return super().on_touch_up(touch)

    def on_checkbox_active(self, instanse):
        if instanse.active:
            if self.product_name not in basket:
                basket.append(self.product_name)
        else:
            if self.product_name in basket:
                basket.remove(self.product_name)


class MainLabel(Label):
    pass


class MainImage(Image):
    pass


class BasketRow(BoxLayout):
    product_name = StringProperty("")
    product_price = StringProperty("")
    product_volume = StringProperty("")
    quantity_box = StringProperty("0")
    box_count = StringProperty("0")

    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and self.product_name:
            app = App.get_running_app()
            item_screen = app.root.get_screen("basket_item")
            item_screen.load_item(self.product_name)
            app.root.current = "basket_item"
            app.root.transition.direction = "left"
        return super().on_touch_up(touch)


class BasketScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def load_basket(self):
        screen = self.manager.get_screen("product_screen")
        products = screen.read_products()
        self.ids.basket_container.clear_widgets()

        for name in basket:
            if name in products:
                info = products[name]
                box_count = get_box_count(name)

                row = BasketRow(
                    product_name=name,
                    product_price=info["price"],
                    product_volume=info["volume"],
                    quantity_box=info["quantity"],
                    box_count=str(box_count),
                )
                self.ids.basket_container.add_widget(row)

    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "up"


class BasketItemScreen(Screen):
    product_name = StringProperty("")
    product_image = StringProperty("")
    quantity_box = StringProperty("0")
    box_count = StringProperty("0")

    def load_item(self, name):
        product_screen = self.manager.get_screen("product_screen")
        products = product_screen.read_products()

        self.product_name = name
        self.product_image = RESOURCES[name]
        self.quantity_box = "0"

        if name in products:
            self.quantity_box = products[name]["quantity"]

        self.box_count = str(get_box_count(name))

    def add_quantity(self):
        count = int(self.box_count)
        if count < 155:
            count += 1
        self.box_count = str(count)
        self.save_boxes()

    def delete_quantity(self):
        count = int(self.box_count)
        if count > 0:
            count -= 1
        self.box_count = str(count)
        self.save_boxes()

    def set_boxes_manual(self, text):
        count = ""
        for ch in text:
            if ch.isdigit:
                count += ch
        if count == "":
            count = "0"
        if count != self.box_count:
            self.box_count = count
            self.save_boxes()

    def save_boxes(self):
        count = int(self.box_count)
        set_box_count(self.product_name, count)

    def goto_basket(self):
        screen = self.manager.get_screen("basket")
        screen.load_basket()
        self.manager.current = "basket"
        self.manager.transition.direction = "right"


class ProductScreen(Screen):
    product_name = StringProperty("")
    product_image = StringProperty("")
    product_quantity = StringProperty("0")
    product_price = StringProperty("")
    product_volume = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)

    def read_products(self):
        with open(PATH_DATA + "list_products.json", "r", encoding="utf8") as file:
            data = json.load(file)
        return data

    def write_products(self, products):
        with open(PATH_DATA + "list_products.json", "w", encoding="utf8") as file:
            json.dump(products, file, ensure_ascii=False, indent=4)

    def load_product(self, name):
        products = self.read_products()

        self.product_name = name
        self.product_image = RESOURCES[self.product_name]
        self.product_quantity = "0"
        self.product_price = ""
        self.product_volume = ""

        if name in products:
            info = products[name]
            self.product_quantity = info["quantity"]
            self.product_price = info["price"]
            self.product_volume = info["volume"]

    def save_quantity(self):
        products = self.read_products()

        if self.product_name in products:
            products[self.product_name]["quantity"] = self.product_quantity

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

        if self.product_name in products:
            del products[self.product_name]

        self.write_products(products)

        if self.product_name in basket:
            basket.remove(self.product_name)

        remove_box_count(self.product_name)

        self.goto_main()

    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "down"


class MenuScreen(Screen):
    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "up"


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.load_resources()

    def load_resources(self):
        with open(PATH_DATA + "list_resources.json", "r", encoding="utf8") as file:
            data = json.load(file)
            RESOURCES.update(data)

    def load_products(self):
        screen = self.manager.get_screen("product_screen")
        products = screen.read_products()
        self.ids.main_container.clear_widgets()
        cb_active = False

        for name in products:
            if name in basket:
                cb_active = True
            else:
                cb_active = False
            # print(name, cb_active)

            bl = BoxRow(
                product_name=name,
                product_price=products[name]["price"],
                product_volume=products[name]["volume"],
                product_quantity=products[name]["quantity"],
                cb_active=cb_active,
            )

            self.ids.main_container.add_widget(bl)

    def on_pre_enter(self, *args):
        self.load_products()
        return super().on_pre_enter(*args)

    def goto_main(self):
        self.manager.current = "menu"
        self.manager.transition.direction = "up"

    def goto_basket(self):
        screen = self.manager.get_screen("basket")
        screen.load_basket()
        self.manager.current = "basket"
        self.manager.transition.direction = "down"


class CompositionApp(App):
    resources = RESOURCES

    def build(self):
        scr_sm = ScreenManager()
        scr_sm.add_widget(MenuScreen(name="menu"))
        scr_sm.add_widget(MainScreen(name="main"))
        scr_sm.add_widget(ProductScreen(name="product_screen"))
        scr_sm.add_widget(BasketScreen(name="basket"))
        scr_sm.add_widget(BasketItemScreen(name="basket_item"))

        return scr_sm


if __name__ == "__main__":

    Window.clearcolor = (0.12, 0.16, 0.22, 1)
    Window.size = (450, 900)

    app = CompositionApp()
    app.run()

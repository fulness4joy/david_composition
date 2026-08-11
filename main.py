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
from datetime import datetime


def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


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


def read_products():
    with open(PATH_DATA + "list_products.json", "r", encoding="utf8") as file:
        data = json.load(file)
    return data


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


class OrderRow(BoxLayout):
    product_name = StringProperty("")
    product_price = StringProperty("")
    product_volume = StringProperty("")
    quantity_box = StringProperty("0")
    box_count = StringProperty("0")

    def on_touch_up(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and self.product_name:
            app = App.get_running_app()
            screen = app.root.get_screen("order")
            screen.load_orders()

        return super().on_touch_up(touch)


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
        products = read_products()
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

    def goto_order(self):
        screen = self.manager.get_screen("order")
        screen.load_orders()
        self.manager.current = "order"
        self.manager.transition.direction = "up"


class BasketItemScreen(Screen):
    product_name = StringProperty("")
    product_image = StringProperty("")
    quantity_box = StringProperty("0")
    box_count = StringProperty("0")

    def load_item(self, name):
        products = read_products()

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

    def write_products(self, products):
        with open(PATH_DATA + "list_products.json", "w", encoding="utf8") as file:
            json.dump(products, file, ensure_ascii=False, indent=4)

    def load_product(self, name):
        products = read_products()

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
        products = read_products()

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
        products = read_products()

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
        products = read_products()
        self.ids.main_container.clear_widgets()
        cb_active = False

        for name in products:
            if name in basket:
                cb_active = True
            else:
                cb_active = False

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


class Order(Screen):
    total_price = StringProperty("0")
    buyer_name = StringProperty("")
    buyer_surname = StringProperty("")
    pack_order = BooleanProperty(False)
    total_volume = StringProperty("0")
    volume_fits = BooleanProperty(True)
    volume_status = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)

    def buyer_details(self, key: str, text: str):
        if key == "name":
            self.buyer_name = text
        elif key == "Фамилия":
            self.buyer_surname = text

    def get_full_name(self):
        full_name = f"{self.buyer_name} {self.buyer_surname}".strip()
        return full_name

    def seller_id(self, full_name):
        sellers_path = PATH_DATA + "sellers.json"
        sellers = read_json(sellers_path)

        if full_name in sellers:
            return sellers[full_name]

        used_ids = []
        for seller in sellers:
            used_ids.append(sellers[seller])

        new_id = 1001
        while new_id in used_ids:
            new_id += 1

        sellers[full_name] = new_id
        write_json(sellers_path, sellers)
        return new_id

    def number_order(self):
        data = read_json(PATH_DATA + "orders.json")
        count = 0
        for seller in data:
            count += len(data[seller])
        return count + 1

    def goto_basket(self):
        screen = self.manager.get_screen("basket")
        screen.load_basket()
        self.manager.current = "basket"
        self.manager.transition.direction = "down"

    def toggle_packing(self, active):
        self.pack_order = active
        self.check_packaging()

    def calc_total_volume(self):
        products = read_products()
        total = 0

        for name in basket:
            if name in products:
                box_count = get_box_count(name)
                if box_count >= 1:
                    quantity = int(products[name]["quantity"])
                    volume = int(products[name]["volume"])
                    total += box_count * quantity * volume

        return total

    def check_packaging(self):
        total = self.calc_total_volume()
        self.total_volume = str(total)
        self.volume_fits = total <= PACKING_BOX_VOLUME

        volume_liters = total / 1000
        if self.volume_fits:
            self.volume_status = ""
        else:
            self.volume_status = (
                f"Не вмещается! {volume_liters} л из 10 л — уберите часть товара"
            )

    def confirm_order(self):
        full_name = self.get_full_name()
        if not full_name:
            return False

        if self.pack_order and not self.volume_fits:
            return False

        items = {}
        for name in basket:
            box_count = get_box_count(name)
            if box_count >= 1:
                items[name] = box_count

        if not items:
            return False

        seller_id = self.seller_id(full_name)
        date = datetime.now().strftime("%d.%m.%Y")
        order_number = self.number_order()

        orders_path = PATH_DATA + "orders.json"
        data = read_json(orders_path)
        seller_key = str(seller_id)
        if seller_key not in data:
            data[seller_key] = {}

        data[seller_key][date] = {
            "order_number": order_number,
            "items": items,
        }
        write_json(orders_path, data)

        products = read_products()
        receipt_items = []
        total = 0
        for name, box_count in items.items():
            if name in products:
                info = products[name]
                price = int(info["price"])
                quantity = int(info["quantity"])
                subtotal = price * quantity * box_count
                total += subtotal
                receipt_items.append(
                    {
                        "name": name,
                        "box_count": str(box_count),
                        "subtotal": str(subtotal),
                    }
                )

        confirm_screen = self.manager.get_screen("order_confirmed")
        confirm_screen.load_item(
            order_number=order_number,
            full_name=full_name,
            date=date,
            items=receipt_items,
            total=str(total),
        )

        basket.clear()
        basket_quantity.clear()
        self.buyer_name = ""
        self.buyer_surname = ""
        self.pack_order = False
        self.total_volume = "0"
        self.volume_fits = True

        self.manager.current = "order_confirmed"
        self.manager.transition.direction = "left"
        return True

    def load_orders(self):
        products = read_products()
        self.ids.order_products.clear_widgets()
        for name in basket:
            if name in products:
                info = products[name]
                box_count = get_box_count(name)

                row = OrderRow(
                    product_name=name,
                    product_price=info["price"],
                    product_volume=info["volume"],
                    quantity_box=info["quantity"],
                    box_count=str(box_count),
                )
                self.ids.order_products.add_widget(row)

        self.total_price = self.sum_price()
        self.check_packaging()

    def sum_price(self) -> str:
        products = read_products()
        total = 0

        for name in basket:
            if name in products:
                box_count = get_box_count(name)
                if box_count >= 1:
                    total += (
                        box_count
                        * int(products[name]["quantity"])
                        * int(products[name]["price"])
                    )

        return str(total)


class OrderConfirmedScreen(Screen):
    order_number = StringProperty("")
    buyer_full_name = StringProperty("")
    order_date = StringProperty("")
    total_price = StringProperty("0")

    def load_item(self, order_number, full_name, date, items, total):
        self.order_number = str(order_number)
        self.buyer_full_name = full_name
        self.order_date = date
        self.total_price = total

    def goto_main(self):
        self.manager.current = "main"
        self.manager.transition.direction = "up"


class CompositionApp(App):
    resources = RESOURCES

    def build(self):
        scr_sm = ScreenManager()
        scr_sm.add_widget(MenuScreen(name="menu"))
        scr_sm.add_widget(MainScreen(name="main"))
        scr_sm.add_widget(ProductScreen(name="product_screen"))
        scr_sm.add_widget(BasketScreen(name="basket"))
        scr_sm.add_widget(BasketItemScreen(name="basket_item"))
        scr_sm.add_widget(Order(name="order"))
        scr_sm.add_widget(OrderConfirmedScreen(name="order_confirmed"))

        return scr_sm


if __name__ == "__main__":

    Window.clearcolor = (0.12, 0.16, 0.22, 1)
    Window.size = (350, 700)
    Window.left = 450
    Window.top = 1

    app = CompositionApp()
    app.stop
    app.run()

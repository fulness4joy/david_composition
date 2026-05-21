from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image


class CompositionApp(App):
    def build(self):
        logo = Image(source = 'assets/images/logo.png', fit_mode='fill')
        button1 = Button(text = "открыть", font_size = "40sp")
        label1 = Label(text = "Склад", font_size = "40sp")

        box = BoxLayout(orientation = "vertical")
        box.add_widget(label1)
        box.add_widget(logo)
        box.add_widget(button1)
        

        return box


app = CompositionApp()
app.run()
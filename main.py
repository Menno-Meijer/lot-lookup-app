import threading

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.card import MDCardSwipe

import lot_lookup as singlelot

Window.size = (325, 650)

class WindowManager(ScreenManager):
    pass

class ExpiryDateWindow(Screen):
    lot_show = ObjectProperty(None)
    exp_show = ObjectProperty(None)
    lot = ObjectProperty(None)
    exp_date = ObjectProperty(None)

    def start_search_thread(self):
        self.ids.spinner.active = True
        singlelot.lot = self.lot.text

        #Reset textinput and displayed text:
        self.lot.text = "B"
        self.exp_show.text = ""
        self.lot_show.text = ""

        #Start thread to not pause the app:
        threading.Thread(target = self.lot_search).start()

    def search_text(self):
        #Display the lot# and expiry date:
        self.exp_show.text = "Exp date: " + self.exp_date
        self.lot_show.text = "Lot#:\n" + singlelot.lot
        Clock.schedule_once(self.add_to_list)

    def lot_search(self):
        self.exp_date = str(singlelot.singlelot_lookup(singlelot.lot))
        self.ids.spinner.active = False
        self.search_text()

    def display_list_page(self):
        self.parent.transition = NoTransition()
        self.parent.current = "ExpiryPageWithList"

    def add_to_list(self, *args):
        self.parent.get_screen("ExpiryPageWithList").ids.md_list.add_widget(
            SwipeToDeleteItem(text=f"{self.lot_show.text}",
                              secondary_text=f"{self.exp_show.text}"))

class ExpiryDateWindowWithList(Screen):
    lot_show = ObjectProperty(None)
    exp_show = ObjectProperty(None)
    lot = ObjectProperty(None)
    exp_date = ObjectProperty(None)


    def start_search_thread(self):
        singlelot.lot = self.lot.text
        #Reset textinput and displayed text:
        self.lot.text = "B"
        self.exp_show.text = ""
        self.lot_show.text = ""

        #Start thread to not pause the app:
        threading.Thread(target = self.lot_search).start()

    def search_text(self):
        #Display the lot# and expiry date:
        self.exp_show.text = "Exp date: " + self.exp_date
        self.lot_show.text = "Lot#:\n" + singlelot.lot
        Clock.schedule_once(self.add_to_list)

    def lot_search(self):
        self.exp_date = str(singlelot.singlelot_lookup(singlelot.lot))
        self.search_text()

    def add_to_list(self, *args):
        self.ids.md_list.add_widget(
            SwipeToDeleteItem(text=f"{self.lot_show.text}",
                              secondary_text=f"{self.exp_show.text}"))

    def display_expiry_page(self):
        self.parent.current = "ExpiryPage"

class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    def remove_item(self, instance):
        app = MDApp.get_running_app().root.get_screen("ExpiryPageWithList")
        app.ids.md_list.remove_widget(instance)

class LotLookupApp(MDApp):

    def build(self):
        Builder.load_file("main.kv")
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Yellow"
        self.theme_cls.accent_hue = "400"
        #self.theme_cls.theme_style = "Dark"
        return WindowManager()


if __name__ == '__main__':
    LotLookupApp().run()
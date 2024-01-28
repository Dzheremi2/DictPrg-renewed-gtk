import sys
import gi
import json
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

dict = {}
with open("dict.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    dict = data

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(850, 600)
        self.set_title('DictPrg')

        self.boxMain = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.boxMain.set_spacing(5)
        self.boxText = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.boxFunc = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.boxFunc.set_spacing(5)
        self.boxBtn = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.boxBtn.set_spacing(5)
        self.scrollWordList = Gtk.ScrolledWindow(propagate_natural_width=True, propagate_natural_height=True)
        self.scrollWordList.set_margin_bottom(10)

        self.set_child(self.boxMain)
        self.boxMain.append(self.boxText)
        self.boxMain.append(self.boxFunc)
        self.boxFunc.append(self.scrollWordList)

        self.TextEditor = Gtk.TextView(hexpand=True)
        self.boxText.append(self.TextEditor)

        self.WordList = Gtk.ListBox(hexpand=True, vexpand=True)
        self.scrollWordList.set_child(self.WordList)

        self.boxFunc.append(self.boxBtn)

        self.addWord = Gtk.Button(label='Add Word', hexpand=True)
        self.boxBtn.append(self.addWord)

        self.rmWord = Gtk.Button(label='Delete Word', hexpand=True)
        self.boxBtn.append(self.rmWord)

        self.saveWord = Gtk.Button(label='Save Word', hexpand=True)
        self.boxFunc.append(self.saveWord)

        #self.button = Gtk.Button(label='hello')
        #self.boxMain.append(self.button)
        #self.button.connect('clicked', self.hello)

        with open("dict.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for key in data:
            self.WordList.append(Gtk.Label(label=key))
        
        def showWord(self, row, TextEditor):
            selectedItem = row.get_child()
            global lable_name
            lable_name = selectedItem.get_text()
            print(dict[lable_name])
            buffer = TextEditor.get_buffer()
            buffer.set_text(dict[lable_name])
            TextEditor.set_buffer(buffer)

        def SaveWord(self, TextEditor):
            buffer = TextEditor.get_buffer()
            buffer = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
            dict[lable_name] = buffer
            with open("dict.json", "w", encoding="utf-8") as file:
                json.dump(dict, file, sort_keys=True, ensure_ascii=False)
                print(dict)

        self.WordList.connect("row-activated", showWord, self.TextEditor)
        self.saveWord.connect("clicked", SaveWord, self.TextEditor)
            

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()
        

app = MyApp(application_id="oss.dzheremi.DictPrg")
app.run(sys.argv)


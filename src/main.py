import sys
import gi
import json
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

sel_row = None
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

        self.addWordBtn = Gtk.Button(label='Add Word', hexpand=True)
        self.boxBtn.append(self.addWordBtn)

        self.rmWord = Gtk.Button(label='Delete Word', hexpand=True)
        self.boxBtn.append(self.rmWord)

        self.saveWord = Gtk.Button(label='Save Word', hexpand=True)
        self.boxFunc.append(self.saveWord)

        def showAddWordDialog(self, WordList, TextEditor):
            dialog = Gtk.Dialog()
            dialog.set_title('Add new word?')
            dialog.set_default_size(300, 130)
            boxDialog = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            boxDialog.set_margin_top(50)
            boxDialog.set_margin_start(10)
            boxDialog.set_margin_end(10)
            dialog.set_child(boxDialog)
            newWordEntry = Gtk.Entry(hexpand=True, vexpand=True)
            boxDialog.append(newWordEntry)
            boxDialogButtons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            boxDialogButtons.set_margin_bottom(50)
            boxDialogButtons.set_margin_end(10)
            boxDialogButtons.set_margin_start(10)
            boxDialogButtons.set_margin_top(20)
            boxDialogButtons.set_spacing(5)
            boxDialog.append(boxDialogButtons)
            addWordCancel = Gtk.Button(hexpand=True)
            cancelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            cancelBox.set_spacing(5)
            iconCancel = Gtk.Image(icon_name='action-unavailable-symbolic')
            cancelLabel = Gtk.Label(label='Cancel')
            cancelBox.append(iconCancel)
            cancelBox.append(cancelLabel)
            addWordCancel.set_child(cancelBox)
            boxDialogButtons.append(addWordCancel)
            addWordOkay = Gtk.Button(hexpand=True)
            okayBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            okayBox.set_spacing(5)
            iconOkay = Gtk.Image(icon_name='object-select-symbolic')
            OkayLable = Gtk.Label(label='Add')
            okayBox.append(iconOkay)
            okayBox.append(OkayLable)
            addWordOkay.set_child(okayBox)
            boxDialogButtons.append(addWordOkay)
            
            dialog.present()

            def showAddWordDialogCancelPressed(self):
                dialog.destroy()

            def showAddWordDialogOkayPressed(self, WordList, TextEditor):
                buffer = newWordEntry.get_buffer()
                buffer = buffer.get_text()
                print(buffer)
                dict[buffer] = ""
                WordList.append(Gtk.Label(label=buffer))
                dialog.destroy()
                SaveWord(self, TextEditor)
                for row in WordList:
                    name = row.get_child()
                    label = name.get_text()
                    if label == buffer:
                        WordList.select_row(row)

            addWordCancel.connect('clicked', showAddWordDialogCancelPressed)
            addWordOkay.connect('clicked', showAddWordDialogOkayPressed, WordList, TextEditor)

        with open("dict.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for key in data:
            self.WordList.append(Gtk.Label(label=key))
        
        
        def showWord(self, row, TextEditor):
            global sel_row
            sel_row = row
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

        def DeleteWord(self, TextEditor, WordList):
            print(sel_row)
            if sel_row is not None:
                with open("dict.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                print(sel_row)
                selectedItem = sel_row.get_child()
                row_data = selectedItem.get_text()
                print(row_data)
                data.pop(row_data)
                with open("dict.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False)
                WordList.remove_all()
                with open("dict.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                for key in data:
                    WordList.append(Gtk.Label(label=key))
                TextEditor.set_buffer(Gtk.TextBuffer().set_text(""))

        self.WordList.connect("row-selected", showWord, self.TextEditor)
        self.WordList.select_row(self.WordList.get_row_at_index(0))
        self.saveWord.connect("clicked", SaveWord, self.TextEditor)
        self.addWordBtn.connect('clicked', showAddWordDialog, self.WordList, self.TextEditor)
        self.rmWord.connect('clicked', DeleteWord, self.TextEditor, self.WordList)
        
            

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()
        

app = MyApp(application_id="oss.dzheremi.DictPrg")
app.run(sys.argv)


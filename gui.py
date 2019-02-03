from tkinter import Tk, Label, Button, Checkbutton, IntVar, Frame
from modules.runner import run, manufacturers

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("BSVP CSV Export")

        self.do_configurator_export = IntVar(value=1);
        self.do_shop_export = IntVar(value=1);
        row = 0

        self.configurator_label = Label(master, text="Konfigurator Export")
        self.configurator_label.grid(sticky="W", row=row)
        row += 1
        self.do_configurator_export_button = Checkbutton(
            master,
            text="Konfigurator Export ausführen",
            variable=self.do_configurator_export
        )
        self.do_configurator_export_button.grid(sticky="W", row=row)
        row += 1

        self.shop_label = Label(master, text="Shop Export")
        self.shop_label.grid(sticky="W", row=row)
        row += 1
        self.do_shop_export_button = Checkbutton(
            master,
            text="Shop Export ausführen",
            variable=self.do_shop_export
        )
        self.do_shop_export_button.grid(sticky="W", row=row)
        row += 1

        self.manufacturers_label = Label(master, text="Hersteller für Shop Export auswählen")
        self.manufacturers_label.grid(sticky="W", row=row)
        row += 1
        self.all_selected = True
        self.manufacturers_start_row = row
        row = self.__manufacturers_gui()

        self.run_button = Button(master, text="Export starten", command=self.run)
        self.run_button.grid(sticky="W", row=row)

    def __manufacturers_gui(self):
        row = self.manufacturers_start_row
        self.__set_select_button_text()
        self.select_button = Button(
            self.master,
            text=self.select_button_text,
            command=self.__toggle_batch_selection,
            width=25
        )
        self.select_button.grid(sticky="W", row=row)
        row += 1
        self.__set_manufacturers()
        self.manufacturer_buttons = {}
        start_row = row
        max_rows = 5
        column = 0
        for manufacturer, value in self.manufacturers.items():
            self.manufacturer_buttons[manufacturer] = Checkbutton(
                self.master,
                text=manufacturer,
                variable=value
            )
            self.manufacturer_buttons[manufacturer].grid(sticky="W", row=row, column=column)
            if row - start_row < max_rows:
                row += 1
            else:
                row = start_row
                column += 1
        return start_row + max_rows + 1


    def __set_manufacturers(self):
        self.manufacturers = {}
        for manufacturer in list(manufacturers.keys()):
            if self.all_selected:
                value = 1
            else:
                value = 0
            self.manufacturers[manufacturer] = IntVar(value=value)

    def __set_select_button_text(self):
        if self.all_selected:
            self.select_button_text = "Alle abwählen"
        else:
            self.select_button_text = "Alle auswählen"

    def __toggle_batch_selection(self):
        self.all_selected = not self.all_selected
        self.__manufacturers_gui()

    def run(self):
        limited_manufacturers = []
        for manufacturer, value in self.manufacturers.items():
            if bool(value.get()):
                limited_manufacturers.append(manufacturer)
        run(
            bool(self.do_configurator_export.get()),
            bool(self.do_shop_export.get()),
            limited_manufacturers
        )

root = Tk()
gui = GUI(root)
root.mainloop()

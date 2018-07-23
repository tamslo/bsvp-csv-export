import os, time, json

class Logger:
    def __init__(self):
        log_file = "exporter.log"
        self.start_time = None
        # Create log file or overwrite old one
        log = open(log_file, "w", encoding="utf-8")
        log.close()
        self.log = open(log_file, "a", encoding="utf-8")
        self.manufacturer = None
        self.products = 0
        self.skips = 0

    def print_start_time(self):
        self.start_time = time.localtime()
        print("")
        print(
            "Export gestartet am {} um {}"
            .format(
                time.strftime("%d.%m.%Y", self.start_time),
                time.strftime("%H:%M", self.start_time)
            )
        )
        print("")

    def print_end_time(self):
        end_time = time.localtime()
        runtime = round(time.mktime(end_time) - time.mktime(self.start_time))
        text = "Export abgeschlossen in "

        if runtime > 120:
            text += " {} Minuten und {} Sekunden".format(runtime//60, runtime % 60)
        else:
            text += "{} Sekunden".format(runtime)

        print("")
        print(text)

    def set_manufacturer(self, manufacturer_name):
        self.manufacturer = manufacturer_name

    def unset_manufacturer(self):
        self.manufacturer = None
        self.products = 0
        self.skips = 0

    def print_manufacturer_progress(self):
        self.products += 1
        print_inline("{} ({})".format(
            self.manufacturer,
            self.products
        ))

    def print_manufacturer_summary(self):
        print_inline(
            "{} ({} gesamt, {} übersprungen)"
            .format(self.manufacturer, self.products, self.skips)
        )
        print("")
        self.unset_manufacturer()

    def log_skip(self, product_name, error_code):
        self.skips += 1
        self.log.write("{} {} {}\n".format(
            self.manufacturer,
            product_name,
            error_code
        ))

def print_inline(text):
    # Overwrite the previous line
    print("                                           ", end="\r")
    print(text, end="\r")

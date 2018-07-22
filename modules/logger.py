import os, time, json

class Logger:
    def __init__(self, product_ending):
        log_file = "exporter.log"
        self.start_time = time.localtime()
        # Create log file or overwrite old one
        log = open(log_file, "w", encoding="utf-8")
        log.close()
        self.log = open(log_file, "a", encoding="utf-8")
        self.product_ending = product_ending
        self.manufacturer = None
        self.products = 0
        self.skips = 0

    def print_start_time(self):
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
        text = "Export abgeschlossen in ".format(runtime)

        if runtime > 120:
            text += " {} Minuten und {} Sekunden".format(runtime//60, runtime % 60)
        else:
            text += "{} Sekunden".format(runtime)

        print("")
        print(text)

    def set_manufacturer(self, manufacturer_name):
        self.manufacturer = manufacturer_name

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
        self.products = 0
        self.skips = 0

    def product_name(self, product_directory):
        return product_directory.split(self.product_ending)[0]

    def log_skip(self, product_directory, error_code):
        self.skips += 1
        self.log.write("{} {} {}\n".format(
            self.manufacturer,
            self.product_name(product_directory),
            error_code
        ))

def print_inline(text):
    # Overwrite the previous line
    print("                                           ", end="\r")
    print(text, end="\r")

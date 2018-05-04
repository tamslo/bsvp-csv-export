import os, time

class Logger:
    def __init__(self, skip_log_file, manufacturer_ending, product_ending):
        self.start_time = time.localtime()
        skip_log = open(skip_log_file, "w", encoding="utf-8")
        skip_log.close()
        self.skip_log = open(skip_log_file, "a", encoding="utf-8")
        self.manufacturer_ending = manufacturer_ending
        self.product_ending = product_ending
        self.manufacturer = None
        self.products = 0
        self.skips = 0

    def print_start_time(self):
        print(
            "Export gestartet am {} um {}"
            .format(
                time.strftime("%d.%m.%Y", self.start_time),
                time.strftime("%H:%M", self.start_time)
            )
        )

    def print_end_time(self):
        end_time = time.localtime()
        runtime = (time.mktime(end_time) - time.mktime(self.start_time))
        print(
            "Export abgeschlossen in {} Sekunden"
            .format(round(runtime))
        )

    def set_manufacturer(self, manufacturer_directory):
        self.manufacturer = self.manufacturer_name(manufacturer_directory)

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

    def manufacturer_name(self, manufacturer_directory):
        return manufacturer_directory.split(self.manufacturer_ending)[0]

    def product_name(self, product_directory):
        return product_directory.split(self.product_ending)[0]

    def log_skip(self, product_directory, error_code):
        self.skips += 1
        self.skip_log.write("{} - {} ({})\n".format(
            self.manufacturer,
            self.product_name(product_directory),
            error_code
        ))

def print_inline(text):
    # Overwrite the previous line
    print("                                           ", end="\r")
    print(text, end="\r")

# -*- coding: utf-8 -*-
import time, json, os
from validator import validate_setup
from exporter import Exporter
from parser import parse_product

# Definition von Konstanten wie Verzeichnissen und Dateiendungen
GENERAL_CONFIG_FILE = "config.json"
EXPORT_CONFIGS_DIRECTORY = "configs/"
MANUFACTURER_ENDING = ".lugg"
PRODUCT_ENDING = ".prod"

# Startzeit merken um Zeit für Export zu messen
start_time = time.time()
print(
    "Export gestartet am {} um {}"
    .format( time.strftime("%d.%m.%Y"), time.strftime("%H:%M"))
)

validate_setup(GENERAL_CONFIG_FILE, EXPORT_CONFIGS_DIRECTORY)

exporter = Exporter(GENERAL_CONFIG_FILE, EXPORT_CONFIGS_DIRECTORY)
exporter.prepare_export()

# BSVP Dateien parsen und in CSV Dateien schreiben

def print_inline(text):
    # Overwrite the previous line
    print("                                           ", end="\r")
    print(text, end="\r")

total_skips = []
with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
    bsvp_data_directory = config["bsvp_data_directory"]
    for manufacturer_directory in os.listdir(bsvp_data_directory):
        if manufacturer_directory.endswith(MANUFACTURER_ENDING):
            manufacturer_path = bsvp_data_directory + manufacturer_directory
            manufacturer = manufacturer_directory.split(MANUFACTURER_ENDING)[0]
            project_directories = os.listdir(manufacturer_path)
            products = 0
            skips = []
            for index, product_directory in enumerate(project_directories):
                if product_directory.endswith(PRODUCT_ENDING):
                    product_path = "/".join([
                        manufacturer_path,
                        product_directory,
                        product_directory
                    ])
                    fields, error_code = parse_product(product_path)
                    products += 1
                    product = product_directory.split(PRODUCT_ENDING)[0]
                    print_inline("{} ({})".format(manufacturer, products))
                    if error_code == None:
                        exporter.write_to_csv(fields)
                    else:
                        skips.append("{} - {} ({})".format(manufacturer, product, error_code))
            print_inline(
                "{} ({} gesamt, {} übersprungen)"
                .format(manufacturer, products, len(skips))
            )
            print("")
            total_skips += skips

with open("skip.log", "w", encoding="utf-8") as skip_file:
    for skip in total_skips:
        skip_file.write(skip + "\n")

# Benötigte Zeit berechnen
end_time = time.time()
runtime = end_time - start_time

print(
    "Export abgeschlossen in {} Sekunden)"
    .format(round(runtime))
)

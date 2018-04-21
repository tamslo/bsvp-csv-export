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

def print_manufacturer(manufacturer_directory):
    manufacturer = manufacturer_directory.split(MANUFACTURER_ENDING)[0]
    print("Hersteller: " + manufacturer)

def print_product(product_directory, end="\r", prefix="Produkt"):
    product = product_directory.split(PRODUCT_ENDING)[0]
    # Overwrite the previous line
    print("                                           ", end="\r")
    print("{}: {}".format(prefix, product), end=end)

with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
    bsvp_data_directory = config["bsvp_data_directory"]
    for manufacturer_directory in os.listdir(bsvp_data_directory):
        if manufacturer_directory.endswith(MANUFACTURER_ENDING):
            print_manufacturer(manufacturer_directory)
            manufacturer_path = bsvp_data_directory + manufacturer_directory
            project_directories = os.listdir(manufacturer_path)
            for index, product_directory in enumerate(project_directories):
                if product_directory.endswith(PRODUCT_ENDING):
                    print_product(product_directory)
                    product_path = "/".join([
                        manufacturer_path,
                        product_directory,
                        product_directory
                    ])
                    fields, error_code = parse_product(product_path)
                    if fields != None:
                        exporter.write_to_csv(fields)
                    else:
                        prefix = "Übersprungen ({})".format(error_code)
                        print_product(product_directory, end="\n", prefix=prefix)

# Benötigte Zeit berechnen
end_time = time.time()
# TODO Zeit nach Stunden, Minuten und Sekunden aufschlüsseln
runtime_in_seconds = end_time - start_time

print("Export abgeschlossen in {} Sekunden".format(runtime_in_seconds))

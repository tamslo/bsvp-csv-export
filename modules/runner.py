import os
import json

from modules.validator import validate_setup
from modules.exporter.configurator import ConfiguratorExporter
from modules.exporter.complete import CompleteExporter
from modules.exporter.shop import ShopExporter
from modules.exporter.price import PriceExporter

GENERAL_CONFIG_FILE = "config.json"
MANUFACTURER_ENDING = ".lugg"
MANUFACTURER_INFO_ENDING = ".ilugg"
PRODUCT_ENDING = ".prod"
PRODUCT_TYPE_ID = "0000191"

# Felder für den Preis Export, mappen auf Felder in der .prod Datei
PRICE_CONFIG = {
    "artikelnummer": "ARTNR",
    "artikelname": "NAME",
    "listenpreis": "PRICE"
}

CONFIGURATOR_NAME = "Konfigurator"
COMPLETE_NAME = "Komplett"
PRICE_NAME = "Listenpreise"
SHOP_NAME = "Shop"

def get_manufacturers():
    with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        bsvp_directory = config["bsvp-ordner"]

    manufacturers = {}
    for manufacturer_directory in os.listdir(bsvp_directory):
        if not manufacturer_directory.endswith(MANUFACTURER_ENDING):
            continue

        manufacturer_path = bsvp_directory + manufacturer_directory
        manufacturer_name = manufacturer_directory.split(MANUFACTURER_ENDING)[0]
        manufacturers[manufacturer_name] = {
            "path": manufacturer_path,
            "products": {}
        }

        for product_directory in os.listdir(manufacturer_path):
            if not product_directory.endswith(PRODUCT_ENDING):
                continue
            product_name = product_directory.split(PRODUCT_ENDING)[0]
            product_path = "/".join([
                manufacturer_path,
                product_directory,
                product_directory
            ])
            manufacturers[manufacturer_name]["products"][product_name] = product_path

    return manufacturers

class Runner:
    def __init__(self):
        validate_setup(GENERAL_CONFIG_FILE, CONFIGURATOR_NAME, SHOP_NAME)
        self.manufacturers = get_manufacturers()
        self.exporters = {
            "configurator": {
                "module": ConfiguratorExporter,
                "running": False,
                "log": None,
                "name": CONFIGURATOR_NAME
            },
            "shop": {
                "module": ShopExporter,
                "running": False,
                "log": None,
                "name": SHOP_NAME
            },
            "price": {
                "module": PriceExporter,
                "running": False,
                "log": None,
                "name": PRICE_NAME
            },
            "complete": {
                "module": CompleteExporter,
                "running": False,
                "log": None,
                "name": COMPLETE_NAME
            }
        }

    def run(self, exporter, selected_manufacturers):
        if not self.exporters[exporter]["running"]:
            self.exporters[exporter]["running"] = True
            print(exporter, flush=True)
            print(selected_manufacturers, flush=True)
            print("Running export", flush=True)
            self.exporters[exporter]["running"] = False

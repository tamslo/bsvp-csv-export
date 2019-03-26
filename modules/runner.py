import os
import json
import logging
from apscheduler.schedulers.background import BackgroundScheduler

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

def parse_manufacturers():
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

        self.manufacturers = parse_manufacturers()
        self.exporters = {
            "configurator": {
                "module": ConfiguratorExporter,
                "scheduled": False,
                "running": False,
                "log": None,
                "name": CONFIGURATOR_NAME
            },
            "shop": {
                "module": ShopExporter,
                "scheduled": False,
                "running": False,
                "log": None,
                "name": SHOP_NAME
            },
            "price": {
                "module": PriceExporter,
                "scheduled": False,
                "running": False,
                "log": None,
                "name": PRICE_NAME
            },
            "complete": {
                "module": CompleteExporter,
                "scheduled": False,
                "running": False,
                "log": None,
                "name": COMPLETE_NAME
            }
        }

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            func=self.check_tasks,
            trigger="interval",
            seconds=8,
            timezone="Europe/Berlin"
        )
        self.running = False
        self.tasks = []
        self.scheduler.start()
        logging.getLogger('apscheduler').setLevel("ERROR")

    def get_manufacturers(self):
        return list(self.manufacturers.keys())

    def get_exporters(self):
        # Module entfernen, kann (und soll) nicht mitgeschickt werden
        sendable_exporters = {}
        for exporter_key, exporter_values in self.exporters.items():
            sendable_exporters[exporter_key] = {
                "name": exporter_values["name"],
                "scheduled": exporter_values["scheduled"],
                "running": exporter_values["running"],
                "log": exporter_values["log"]
            }
        return sendable_exporters

    def check_tasks(self):
        if not self.running and len(self.tasks) > 0:
            self.run(self.tasks.pop(0))

    def add_task(self, exporter, selected_manufacturers):
        if not self.exporters[exporter]["scheduled"]:
            self.tasks.append({
                "exporter": exporter,
                "selected_manufacturers": selected_manufacturers
            })
            self.mark_scheduled(exporter)
        return self.get_exporters()

    def mark_scheduled(self, exporter):
        self.exporters[exporter]["scheduled"] = True
        self.exporters[exporter]["log"] = ["Export zu Aufgaben hinzugefügt"]

    def run(self, task):
        exporter = task["exporter"]
        selected_manufacturers = task["selected_manufacturers"]
        if not self.exporters[exporter]["running"]:
            self.exporters[exporter]["scheduled"] = False
            self.exporters[exporter]["running"] = True
            self.exporters[exporter]["module"](self.manufacturers).run(selected_manufacturers)
            self.exporters[exporter]["running"] = False

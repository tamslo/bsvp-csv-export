import os
import json
import logging
import time
from datetime import datetime
import shutil

from apscheduler.schedulers.background import BackgroundScheduler
from modules.constants import GENERAL_CONFIG_FILE, MANUFACTURER_ENDING, \
    MANUFACTURER_INFO_ENDING, PRODUCT_ENDING, PRODUCT_TYPE_ID, \
    CONFIGURATOR_NAME, SHOP_NAME, PRICE_NAME, COMPLETE_NAME

from modules.parser.prod import parse_product
from modules.parser.ilugg import parse_manufacturer_information
from modules.exporter.configurator import ConfiguratorExporter
from modules.exporter.complete import CompleteExporter
from modules.exporter.shop import ShopExporter
from modules.exporter.price import PriceExporter
from modules.logger import Logger

def write_skip_log(logger, file, error):
    logger.log(file + ": " + error)


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
            if not product_directory.endswith(PRODUCT_ENDING) or product_directory == PRODUCT_ENDING:
                continue
            product_name = product_directory.split(PRODUCT_ENDING)[0]
            product_path = "/".join([
                manufacturer_path,
                product_directory,
                product_directory
            ])
            manufacturers[manufacturer_name]["products"][product_name] = product_path

    return manufacturers

def get_manufacturer_information(manufacturer_path, manufacturer_name):
    ilugg_path = manufacturer_path + "/" + manufacturer_name + MANUFACTURER_INFO_ENDING
    if not os.path.exists(ilugg_path):
        return None, "NICHT_VORHANDEN"
    manufacturer_information = parse_manufacturer_information(ilugg_path)
    if not manufacturer_information:
        return None, "NICHT_AUSWERTBAR"
    return manufacturer_information, None

def get_time():
    return time.strftime("%H:%M:%S", time.localtime())

class Runner:
    def __init__(self):
        self.manufacturers = parse_manufacturers()
        self.exporters = {
            "configurator": {
                "module": ConfiguratorExporter(self.manufacturers),
                "scheduled": False,
                "running": False,
                "log": [],
                "name": CONFIGURATOR_NAME
            },
            "shop": {
                "module": ShopExporter(self.manufacturers),
                "scheduled": False,
                "running": False,
                "log": [],
                "name": SHOP_NAME
            },
            "price": {
                "module": PriceExporter(self.manufacturers),
                "scheduled": False,
                "running": False,
                "log": [],
                "name": PRICE_NAME
            },
            "complete": {
                "module": CompleteExporter(self.manufacturers),
                "scheduled": False,
                "running": False,
                "log": [],
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
            last_export_date = exporter_values["module"].last_export_date(exporter_values["running"])
            if last_export_date != None:
                last_export_date = datetime.utcfromtimestamp(last_export_date).strftime("%d.%m.%Y")
            sendable_exporters[exporter_key] = {
                "name": exporter_values["name"],
                "scheduled": exporter_values["scheduled"],
                "running": exporter_values["running"],
                "log": exporter_values["log"],
                "last": last_export_date
            }
        return sendable_exporters

    def check_tasks(self):
        if not self.running and len(self.tasks) > 0:
            self.run(self.tasks.pop(0))

    def add_task(self, exporter, selected_manufacturers):
        if self.exporters[exporter]["scheduled"]:
            return "SCHEDULED"
        if self.exporters[exporter]["running"]:
            return "RUNNING"

        self.tasks.append({
            "exporter": exporter,
            "selected_manufacturers": selected_manufacturers
        })
        self.exporters[exporter]["scheduled"] = True
        self.exporters[exporter]["log"] = ["Export um {} zur Warteschlange hinzugefügt".format(get_time())]

        # Wenn Hersteller eingeschränkt werden können, sollen diese
        # angezeigt werden
        exporter_module = self.exporters[exporter]["module"]
        show_selected_manufacturers = exporter_module.should_skip("Not a manufacturer", selected_manufacturers)
        if show_selected_manufacturers:
            self.exporters[exporter]["log"].append(
                "Ausgewählte Hersteller: {}".format(", ".join(selected_manufacturers))
            )
        return None

    def run(self, task):
        exporter_id = task["exporter"]
        selected_manufacturers = task["selected_manufacturers"]
        exporter = self.exporters[exporter_id]
        exporter_module = exporter["module"]
        logger = Logger()
        logger.set_path(exporter_id)
        if not exporter["running"]:
            exporter["scheduled"] = False
            exporter["running"] = True

            start_text = "Export gestartet um {}".format(get_time())
            exporter["log"].append(start_text)
            logger.log(start_text)
            exporter_module.setup()

            # Variablen für Log
            current_manufacturer = None
            current_product_number = None
            current_product_skips = None

            for manufacturer_name, manufacturer in self.manufacturers.items():
                # Log Variablen anpassen
                current_manufacturer = manufacturer_name
                current_product_number = 0
                current_product_skips = 0

                manufacturer_path = manufacturer["path"]
                if exporter_module.should_skip(manufacturer_name, selected_manufacturers):
                    continue

                logger.log("\n{}".format(current_manufacturer))
                exporter["log"].append(current_manufacturer)

                manufacturer_information = None
                if exporter_module.uses_manufacturer_information():
                    manufacturer_information, error_code = get_manufacturer_information(
                        manufacturer_path,
                        manufacturer_name
                    )
                    if error_code != None:
                        exporter["log"][-1] = "{} übersprungen, ILUGG Datei konnte nicht gelesen werden".format(current_manufacturer)
                        write_skip_log(logger, "ILUGG", error_code)
                        continue

                for product_name, product_path in manufacturer["products"].items():
                    current_product_number += 1
                    exporter["log"][-1] = "{} ({})".format(
                        current_manufacturer,
                        current_product_number
                    )
                    if not os.path.exists(product_path):
                        current_product_skips += 1
                        write_skip_log(logger, product_name, "PROD_UNTERSCHIEDLICH")
                        continue

                    fields, attribute_names, attribute_types, error_code = parse_product(product_path)
                    if error_code != None:
                        current_product_skips += 1
                        write_skip_log(logger, product_name, error_code)
                        continue

                    error_code = exporter_module.write_to_csv({
                        "fields": fields,
                        "attribute_names": attribute_names,
                        "attribute_types": attribute_types,
                        "manufacturer_name": manufacturer_name,
                        "manufacturer_information": manufacturer_information
                    })
                    if error_code != None:
                        current_product_skips += 1
                        write_skip_log(logger, product_name, error_code)

                exporter["log"][-1] = "{} ({} gesamt, {} übersprungen)".format(
                    current_manufacturer,
                    current_product_number,
                    current_product_skips
                )

            end_text = "Export beended um {}".format(get_time())
            logger.log("\n" + end_text)
            exporter["log"].append(end_text)
            exporter["running"] = False

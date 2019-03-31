import os
import json
import logging
import time
import shutil

from apscheduler.schedulers.background import BackgroundScheduler
from modules.constants import GENERAL_CONFIG_FILE, ARCHIVE_DIRECTORY, \
    MANUFACTURER_ENDING, MANUFACTURER_INFO_ENDING, PRODUCT_ENDING, \
    PRODUCT_TYPE_ID, SKIP_LOG_FILE, CONFIGURATOR_NAME, SHOP_NAME, PRICE_NAME, \
    COMPLETE_NAME

from modules.parser.prod import parse_product
from modules.validator import validate_fields
from modules.exporter.configurator import ConfiguratorExporter
from modules.exporter.complete import CompleteExporter
from modules.exporter.shop import ShopExporter
from modules.exporter.price import PriceExporter

def write_skip_log(file_name, manufacturer, file, error):
    with open(file_name, "a", encoding="utf-8") as log:
        log.write("{} {} {}\n".format(
            manufacturer,
            file,
            error
        ))


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

def get_manufacturer_information(manufacturer_path, manufacturer_name):
    ilugg_path = manufacturer_path + "/" + manufacturer_name + MANUFACTURER_INFO_ENDING
    if not os.path.exists(ilugg_path):
        return None, "NICHT_VORHANDEN"
    manufacturer_information = parse_manufacturer_information(ilugg_path)
    if not manufacturer_information:
        return None, "NICHT_AUSWERTBAR"
    return manufacturer_information, None

# Hilfsmethode, entpackt verschachtelte Felder wie TECHDATA
def flatten_fields(fields):
    flattened_fields = {}
    for field_name, field_value in fields.items():
        if isinstance(field_value, str):
            flattened_fields[field_name] = field_value
        else:
            for attribute_name, attribute_value in field_value.items():
                flattened_fields[attribute_name] = attribute_value
    return flattened_fields

class Runner:
    def __init__(self):
        self.manufacturers = parse_manufacturers()
        self.exporters = {
            "configurator": {
                "module": ConfiguratorExporter,
                "scheduled": False,
                "running": False,
                "log": [],
                "name": CONFIGURATOR_NAME
            },
            "shop": {
                "module": ShopExporter,
                "scheduled": False,
                "running": False,
                "log": [],
                "name": SHOP_NAME
            },
            "price": {
                "module": PriceExporter,
                "scheduled": False,
                "running": False,
                "log": [],
                "name": PRICE_NAME
            },
            "complete": {
                "module": CompleteExporter,
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
            self.exporters[exporter]["scheduled"] = True
            self.exporters[exporter]["log"].append("Export zu Aufgaben hinzugefügt")
        return self.get_exporters()

    def prepare_run(self, exporter_module, exporter):
        # Wenn es bereits einen Export gibt, wird dieser archiviert, sonst
        # erstellt
        output_directory = exporter_module.output_directory()
        if os.path.exists(output_directory):
            archive_base_directory = exporter_module.config["export-ordner"] + ARCHIVE_DIRECTORY + "/"
            if not os.path.exists(archive_base_directory):
                os.makedirs(archive_base_directory)

            archive_directory = archive_base_directory + exporter_module.name() + "/"
            if os.path.exists(archive_directory):
                shutil.rmtree(archive_directory)

            shutil.move(output_directory, archive_directory)
            exporter["log"].append("Letzer Export wurde archiviert")
        os.makedirs(output_directory)
        exporter["log"].append("Export Verzeichnis wurde erstellt")

    def run(self, task):
        exporter_id = task["exporter"]
        selected_manufacturers = task["selected_manufacturers"]
        exporter = self.exporters[exporter_id]
        exporter_module = exporter["module"](self.manufacturers)
        skip_log_file_name = ("{}_{}_{}".format(int(time.time()), exporter, SKIP_LOG_FILE))
        if not exporter["running"]:
            exporter["scheduled"] = False
            exporter["running"] = True

            exporter["log"].append("Export gestartet um {}".format(time.strftime("%H:%M", time.localtime())))
            self.prepare_run(exporter_module, exporter)

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

                exporter["log"].append(current_manufacturer)

                manufacturer_information = None
                if exporter_module.uses_manufacturer_information():
                    manufacturer_information, error_code = get_manufacturer_information(
                        manufacturer_path,
                        manufacturer_name
                    )
                    if error_code != None:
                        exporter["log"][-1] = "{} übersprungen".format(current_manufacturer)
                        write_skip_log(skip_log_file_name, manufacturer_name, "ILUGG", error_code)
                        continue

                for product_name, product_path in manufacturer["products"].items():
                    current_product_number += 1
                    exporter["log"][-1] = "{} ({})".format(
                        current_manufacturer,
                        current_product_number
                    )
                    if not os.path.exists(product_path):
                        current_product_skips += 1
                        write_skip_log(skip_log_file_name, manufacturer_name, product_name, "PROD_UNTERSCHIEDLICH")
                        continue

                    fields, attribute_names, attribute_types = parse_product(product_path)
                    error_code = validate_fields(fields, PRODUCT_TYPE_ID)
                    if error_code != None:
                        current_product_skips += 1
                        write_skip_log(skip_log_file_name, manufacturer_name, product_name, error_code)
                        continue
                    flattened_fields = flatten_fields(fields)
                    product_type = flattened_fields[PRODUCT_TYPE_ID]

                    error_code = exporter_module.write_to_csv({
                        "fields": fields,
                        "attribute_names": attribute_names,
                        "attribute_types": attribute_types,
                        "flattened_fields": flattened_fields,
                        "product_type": product_type,
                        "manufacturer_name": manufacturer_name,
                        "manufacturer_information": manufacturer_information
                    })

                    if error_code != None:
                        current_product_skips += 1
                        write_skip_log(skip_log_file_name, manufacturer_name, product_name, error_code)

                exporter["log"][-1] = "{} ({} gesamt, {} übersprungen)".format(
                    current_manufacturer,
                    current_product_number,
                    current_product_skips
                )

            exporter["log"].append("Export beended um {}".format(time.strftime("%H:%M", time.localtime())))

            self.exporters[exporter]["running"] = False

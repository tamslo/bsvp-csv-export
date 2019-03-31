import csv
import json
import os
import shutil
from modules.constants import GENERAL_CONFIG_FILE

class BaseExporter:
    def __init__(self, manufacturers):
        with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)
            self.manufacturers = manufacturers
            self.shop_csv_separator = self.config["shop-csv-separator"]
            self.configurator_csv_separator = self.config["konfigurator-csv-separator"]
            self.csv_encoding = self.config["csv-encoding"]
            self.configs_base_directory = self.config["configs-ordner"]
            self.bsvp_directory = self.config["bsvp-ordner"]
            self.tooltip_path = self.config["tooltip-datei"]

    def name(self):
        raise Exception("BaseExporter::name needs to be implemented by extending classes")

    def output_directory(self):
        return self.config["export-ordner"] + self.name() + "/"

    def should_skip(self, manufacturer_name, selected_manufacturers):
        return not manufacturer_name in selected_manufacturers

    def uses_manufacturer_information(self):
        return False

    def maybe_create_csv(self, path, header_fields):
        if not os.path.exists(path):
            self.write_csv_row(path, header_fields, file_mode="w")

    def write_csv_row(self, path, row, file_mode="a"):
        with open(path, file_mode, encoding=self.csv_encoding, newline="") as file:
            csv_writer = csv.writer(file, delimiter=self.csv_separator)
            csv_writer.writerow(row)

    def write_to_csv(self, **args):
        raise Exception("BaseExporter::write_to_csv needs to be implemented by extending classes")

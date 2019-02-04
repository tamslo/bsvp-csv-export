import csv
import json
import os

class BaseExporter:
    def __init__(self, general_config_file, exporter_name):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.shop_csv_separator = general_config["shop-csv-separator"]
            self.configurator_csv_separator = general_config["konfigurator-csv-separator"]
            self.csv_encoding = general_config["csv-encoding"]
            self.configs_base_directory = general_config["configs-ordner"]
            self.bsvp_directory = general_config["bsvp-ordner"]
            self.tooltip_path = general_config["tooltip-datei"]
            self.output_directory = general_config["export-ordner"] + exporter_name + "/"
            self.__setup()

    def __setup(self):
        # Erstelle das Verzeichnis in das exportiert werden soll, wenn noch
        # nicht vorhanden
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def maybe_create_csv(self, path, header_fields):
        if not os.path.exists(path):
            self.write_csv_row(path, header_fields, file_mode="w")

    def write_csv_row(self, path, row, file_mode="a"):
        with open(path, file_mode, encoding=self.csv_encoding, newline="") as file:
            csv_writer = csv.writer(file, delimiter=self.csv_separator)
            csv_writer.writerow(row)

    def write_to_csv(self, **args):
        raise Exception("BaseExporter::write_to_csv needs to be implemented by extending classes")

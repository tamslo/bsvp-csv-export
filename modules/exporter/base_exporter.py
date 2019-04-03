import csv
import json
import os
import shutil
from modules.constants import GENERAL_CONFIG_FILE, ARCHIVE_DIRECTORY

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

    def __archive_base_directory(self):
        return self.config["export-ordner"] + ARCHIVE_DIRECTORY + "/"

    def __archive_directory(self):
        return self.__archive_base_directory() + self.name() + "/"

    def should_skip(self, manufacturer_name, selected_manufacturers):
        return not manufacturer_name in selected_manufacturers

    def uses_manufacturer_information(self):
        return False

    def last_export_date(self, running):
        last_export_folder = None
        if running:
            last_export_folder = self.__archive_directory()
        else:
            last_export_folder = self.output_directory()
        if os.path.exists(last_export_folder):
            return os.path.getmtime(last_export_folder)
        else:
            return None

    def setup(self):
        # Wenn es bereits einen Export gibt, wird dieser archiviert, sonst
        # erstellt
        output_directory = self.output_directory()
        if os.path.exists(output_directory):
            archive_base_directory = self.__archive_base_directory()
            if not os.path.exists(archive_base_directory):
                os.makedirs(archive_base_directory)

            archive_directory = self.__archive_directory()
            if os.path.exists(archive_directory):
                shutil.rmtree(archive_directory)

            shutil.move(output_directory, archive_directory)
        os.makedirs(output_directory)

    def maybe_create_csv(self, path, header_fields):
        if not os.path.exists(path):
            self.write_csv_row(path, header_fields, file_mode="w")

    def write_csv_row(self, path, row, file_mode="a"):
        with open(path, file_mode, encoding=self.csv_encoding, newline="") as file:
            csv_writer = csv.writer(file, delimiter=self.csv_separator)
            try:
                csv_writer.writerow(row)
                return None
            except UnicodeEncodeError as error:
                return "WRITE_ERROR: {}".format(error)

    def write_to_csv(self, **args):
        raise Exception("BaseExporter::write_to_csv needs to be implemented by extending classes")

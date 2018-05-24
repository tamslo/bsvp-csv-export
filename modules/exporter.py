# -*- coding: utf-8 -*-
import os, shutil, json, csv
from collections import OrderedDict

class Exporter:
    def __init__(self, general_config_file):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.csv_separator = general_config["separator"]
            self.csv_encoding = general_config["encoding"]
            self.csv_line_ending = general_config["line_ending"]
            self.output_directory = general_config["output_directory"]
            self.archive_directory = general_config["archive_directory"]
            self.configs_directory = general_config["configs_directory"]
            self.configs = self.__transform_configs()
            self.__setup()

    def __transform_configs(self):
        configs = {}
        for export_config_name in os.listdir(self.configs_directory):
            if export_config_name.endswith(".json"):
                product_type, config = self.__transform_config(export_config_name)
                configs[product_type] = config
        return configs

    def __transform_config(self, export_config_name):
        export_config_path = self.configs_directory + export_config_name
        with open(export_config_path, "r",  encoding="utf-8") as export_config_file:
            export_config = json.load(export_config_file, object_pairs_hook=OrderedDict)
            output_file_name = export_config_name.split(".json")[0] + ".csv"
            if not "kombinationen" in export_config:
                export_config["kombinationen"] = {}
            export_config["pfad"] = self.output_directory + output_file_name
            return export_config["produkttyp"], export_config

    def __setup(self):
        # Erstelle das Verzeichnis in das exportiert werden soll, wenn noch
        # nicht vorhanden
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Wenn es bereits Dateien im Output-Verzeichnis gibt, werden diese
        # archiviert. Entweder gibt es schon einen Archiv-Ordner, der gelöscht
        # und neu angelegt wird, oder der Ornder wird erstellt. Dann werden die
        # vorhandenen Dateien in den Ordner kopiert.
        if len([file for file in os.listdir(self.output_directory) if is_csv(file)]) != 0:
            if not os.path.exists(self.archive_directory):
                os.makedirs(self.archive_directory)
                move_csv_files(self.output_directory, self.archive_directory)
            else:
                shutil.rmtree(self.archive_directory)
                os.makedirs(self.archive_directory)
                move_csv_files(self.output_directory, self.archive_directory)

        # Erstelle die CSV Dateien und schreibe die festgelegten Attribute als
        # Header
        for config in list(self.configs.values()):
            with open(config["pfad"], "w", encoding=self.csv_encoding, newline="") as file:
                csv_writer = csv.writer(
                    file,
                    delimiter=self.csv_separator,
                    lineterminator=self.csv_line_ending
                )
                header_fields = []
                fields = config["felder"]
                for field in list(fields.keys()):
                    field_value = fields[field]
                    if isinstance(field_value, str):
                        header_fields.append(field_value)
                    else:
                        header_fields += list(field_value.values())
                header_fields += list(config["kombinationen"].keys())
                csv_writer.writerow(header_fields)

    def write_to_csv(self, fields, product_type_id):
        product_type = fields[product_type_id]
        delivery_status = fields["DELSTAT"]
        active_delivery_statuses = ["0", "1", "2", "3", "4"]
        if product_type in self.configs and delivery_status in active_delivery_statuses:
            config = self.configs[product_type]
            with open(config["pfad"], "a", encoding=self.csv_encoding, newline="") as file:
                csv_writer = csv.writer(file, delimiter=self.csv_separator)
                product_information = extract_product_information(config, fields)
                csv_writer.writerow(product_information)

def get_field(config, fields, field_name):
    if field_name in fields:
        return fields[field_name]
    else:
        return None

def extract_product_information(config, fields):
    product_information = []

    # Spezifizierte Felder in product_information schreiben
    for field_name in config["felder"]:
        field_value = config["felder"][field_name]
        product_information.append(get_field(config, fields, field_name))

    # Spezifizierte Kominationen bilden und in product_information schreiben
    for name, combination in config["kombinationen"].items():
        fields = list(map(
            lambda field_name: get_field(config, fields, field_name) or "",
            combination["felder"]
        ))
        if all(field == "" for field in fields):
            product_information.append(None)
        else:
            product_information.append(combination["separator"].join(fields))

    return product_information

def is_csv(file):
    return file.endswith(".csv")

def move_csv_files(origin, destination):
    for file in os.listdir(origin):
        if is_csv(file):
            current_path = "{}/{}".format(origin, file)
            new_path = "{}/{}".format(destination, file)
            shutil.move(current_path, new_path)

# -*- coding: utf-8 -*-
import os, shutil, json, csv
from collections import OrderedDict

class Exporter:
    def __init__(self, general_config_file):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.archive_name = "Archiv"
            self.csv_separator = general_config["konfigurator-csv-separator"]
            self.csv_encoding = general_config["csv-encoding"]
            self.output_directory = general_config["export-ordner"]
            self.archive_directory = self.output_directory + self.archive_name
            self.configs_directory = general_config["configs-ordner"] + "Konfigurator/"
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
            config_name = self.output_directory + export_config_name.split(".json")[0]
            base_output_path = config_name + ".csv"
            export_config["outputs"] = [{ "base": True, "path": base_output_path }]
            if "hersteller_export" in export_config:
                for manufacturer in export_config["hersteller_export"]:
                    manufacturer_output_path = "{}_{}.csv".format(
                        config_name,
                        manufacturer
                    )
                    export_config["outputs"].append({
                        "base": False,
                        "manufacturer": manufacturer,
                        "path": manufacturer_output_path
                    })
            if not "kombinationen" in export_config:
                export_config["kombinationen"] = {}
            return export_config["produkttyp"], export_config

    def __archive_export(self):
        for file in os.listdir(self.output_directory):
            if file != self.archive_name:
                current_path = "{}/{}".format(self.output_directory, file)
                new_path = "{}/{}".format(self.archive_directory, file)
                shutil.move(current_path, new_path)

    def __setup(self):
        # Erstelle das Verzeichnis in das exportiert werden soll, wenn noch
        # nicht vorhanden
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Wenn es bereits Dateien im Output-Verzeichnis gibt, werden diese
        # archiviert. Entweder gibt es schon einen Archiv-Ordner, der gelöscht
        # und neu angelegt wird, oder der Ornder wird erstellt. Dann werden die
        # vorhandenen Dateien in den Ordner kopiert.
        if len([file for file in os.listdir(self.output_directory) if file != self.archive_name]) != 0:
            if os.path.exists(self.archive_directory):
                shutil.rmtree(self.archive_directory)
            os.makedirs(self.archive_directory)
            self.__archive_export()

        # Erstelle die CSV Dateien und schreibe die festgelegten Attribute als
        # Header
        for config in list(self.configs.values()):
            for output in config["outputs"]:
                with open(output["path"], "w", encoding=self.csv_encoding, newline="") as file:
                    csv_writer = csv.writer(
                        file,
                        delimiter=self.csv_separator
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
        manufacturer = fields["MANUFACTURER"]
        delivery_status = fields["DELSTAT"]
        active_delivery_statuses = ["0", "1", "2", "3", "4"]
        if product_type in self.configs and delivery_status in active_delivery_statuses:
            config = self.configs[product_type]
            for output in config["outputs"]:
                with open(output["path"], "a", encoding=self.csv_encoding, newline="") as file:
                    if output["base"] or output["manufacturer"] == manufacturer:
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

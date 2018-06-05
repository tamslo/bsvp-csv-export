# -*- coding: utf-8 -*-
import os, json, csv
from modules.configurator.configs import transform_configs
from modules.configurator.formatter import format_field

class ConfiguratorExporter:
    def __init__(self, general_config_file, configurator_name):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.csv_separator = general_config["konfigurator-csv-separator"]
            self.csv_encoding = general_config["csv-encoding"]
            self.output_directory = general_config["export-ordner"] + configurator_name + "/"
            self.configs_directory = general_config["configs-ordner"] + configurator_name + "/"
            self.configs = transform_configs(self.configs_directory, self.output_directory)
            self.__setup()

    def __setup(self):
        # Erstelle das Verzeichnis in das exportiert werden soll, wenn noch
        # nicht vorhanden
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

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

    def write_to_csv(self, fields, product_type):
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
        return format_field(config["formatierungen"], fields[field_name], field_name)
    else:
        return None

def extract_product_information(config, fields):
    product_information = []

    # Spezifizierte Felder in product_information schreiben
    for field_name, field_value in config["felder"].items():
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

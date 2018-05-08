# -*- coding: utf-8 -*-
import os, shutil, json, csv
from collections import OrderedDict
from formatter import format_value

class Exporter:
    def __init__(self, general_config_file):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.csv_separator = general_config["separator"]
            self.csv_encoding = general_config["encoding"]
            self.csv_line_ending = general_config["line_ending"]
            self.output_directory = general_config["output_directory"]
            self.archive_directory = general_config["archive_directory"]
            self.configs = build_configs(general_config["configs_directory"])

    def csv_path(self, config):
        return self.output_directory + config["file_name"]

    def prepare_export(self):
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
            csv_path = self.csv_path(config)
            with open(csv_path, "w", encoding=self.csv_encoding, newline="") as csv_file:
                csv_writer = csv.writer(
                    csv_file,
                    delimiter=self.csv_separator,
                    lineterminator=self.csv_line_ending
                )
                header_fields = []
                fields = config["fields"]
                for field in list(fields.keys()):
                    field_value = fields[field]
                    if isinstance(field_value, str):
                        header_fields.append(field_value)
                    else:
                        header_fields += list(field_value.values())
                header_fields += list(config["combinations"].keys())
                csv_writer.writerow(header_fields)

    def write_to_csv(self, fields, product_type_id):
        product_type = fields["TECHDATA"][product_type_id]
        if product_type in self.configs:
            config = self.configs[product_type]
            csv_path = self.csv_path(config)
            with open(csv_path, "a", encoding=self.csv_encoding, newline="") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=self.csv_separator)
                product_information = extract_product_information(config, fields)
                csv_writer.writerow(product_information)

def get_field(config, fields, field_name):
    if field_name in fields:
        return format_value(config["format_options"], field_name, fields[field_name])
    else:
        return None

def extract_product_information(config, fields):
    product_information = []

    # Spezifizierte Felder in product_information schreiben
    for field_name in config["fields"]:
        field_value = config["fields"][field_name]
        # Wenn der field_value ein einfaches Feld ist (z.B ARTNR), dann ist der Wert ein
        # String und kann direkt in die product_information geschrieben werden. Ansonsten
        # wird über die Attribute iteriert (z.B in TECHDATA).
        if isinstance(field_value, str):
            product_information.append(get_field(config, fields, field_name))
        else:
            for attribute_name in list(field_value.keys()):
                product_information.append(
                    get_field(config, fields[field_name], attribute_name)
                )

    # Spezifizierte Kominationen bilden und in product_information schreiben
    for name, combination in config["combinations"].items():
        field_name = combination["feld"]
        fields = list(map(
            lambda attribute_name: get_field(config, fields[field_name], attribute_name) or "",
            combination["felder"]
        ))
        if all(field == "" for field in fields):
            product_information.append(None)
        else:
            product_information.append(combination["separator"].join(fields))

    return product_information

def build_config(export_config_name, export_configs_directory):
    export_config_path = export_configs_directory + export_config_name
    with open(export_config_path, "r",  encoding="utf-8") as export_config_file:
        export_config = json.load(export_config_file, object_pairs_hook=OrderedDict)
        output_file_name = export_config_name.split(".json")[0] + ".csv"
        product_type = export_config["produkttyp"]
        fields = export_config["felder"]
        combinations = export_config["kombinationen"] if "kombinationen" in export_config else {}
        format_options = export_config["formatierungen"] if "formatierungen" in export_config else {}
        config = {
            "file_name": output_file_name,
            "fields": fields,
            "combinations": combinations,
            "format_options": format_options
        }
        return product_type, config

def build_configs(export_configs_directory):
    configs = {}
    for export_config_name in os.listdir(export_configs_directory):
        if export_config_name.endswith(".json"):
            product_type, config = build_config(export_config_name, export_configs_directory)
            configs[product_type] = config
    return configs

def is_csv(file):
    return file.endswith(".csv")

def move_csv_files(origin, destination):
    for file in os.listdir(origin):
        if is_csv(file):
            current_path = "{}/{}".format(origin, file)
            new_path = "{}/{}".format(destination, file)
            shutil.move(current_path, new_path)

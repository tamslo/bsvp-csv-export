# -*- coding: utf-8 -*-
import os, json, csv
from modules.parser.tooltips import parse_tooltips
from .description import export_description
from .energy_efficiency_text import export_energy_efficiency_text
from .video import export_video

special_cases = {
    "p_desc.de": export_description,
    "products_energy_efficiency_text": export_energy_efficiency_text,
    "p_movies.de": export_video
}

def special_case_names():
    return list(special_cases.keys())

class ShopExporter:
    def __init__(self, general_config_file, shop_name, manufacturer_ending):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.tooltips = parse_tooltips(general_config["tooltip-datei"])
            self.csv_separator = general_config["shop-csv-separator"]
            self.csv_encoding = general_config["csv-encoding"]
            self.output_directory = general_config["export-ordner"] + shop_name + "/"
            self.bsvp_directory = general_config["bsvp-ordner"]
            self.manufacturer_ending = manufacturer_ending
            export_config_path = general_config["configs-ordner"] + shop_name + ".json"
            with open(export_config_path, "r", encoding="utf-8") as export_config_file:
                self.config = json.load(export_config_file)
            self.__setup()

    def __csv_path(self, manufacturer_directory):
        manufacturer_name = manufacturer_directory.split(self.manufacturer_ending)[0]
        return self.output_directory + manufacturer_name + ".csv"

    def __setup(self):
        # Erstelle das Verzeichnis in das exportiert werden soll, wenn noch
        # nicht vorhanden
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def __header_fields(self, prod_fields, ilugg_fields):
        header_fields = []
        for field_name, value_specification in self.config.items():
            if "iterierbar" in value_specification:
                def make_header_field(specification, index):
                    header_fields.append(field_name + str(index))
                self.__iterate(value_specification, prod_fields, ilugg_fields, make_header_field)
            else:
                header_fields.append(field_name)

        return header_fields

    def __iterate(self, value_specification, prod_fields, ilugg_fields, callback):
        specification = value_specification["iterierbar"]
        max = int(self.__get_value(
            specification["max"],
            prod_fields,
            ilugg_fields
        ))
        start = 0 if not "start" in specification else int(specification["start"])
        while start < max:
            callback(specification, start)
            start += 1

    def __create_csv(self, path, prod_fields, ilugg_fields):
        with open(path, "w", encoding=self.csv_encoding, newline="") as file:
            csv_writer = csv.writer(
                file,
                delimiter=self.csv_separator
            )
            header_fields = self.__header_fields(prod_fields, ilugg_fields)
            csv_writer.writerow(header_fields)

    def write_to_csv(self, prod_fields, attribute_names, ilugg_fields, manufacturer_directory):
        csv_path = self.__csv_path(manufacturer_directory)

        if not os.path.exists(csv_path):
            self.__create_csv(csv_path, prod_fields, ilugg_fields)

        with open(csv_path, "a", encoding=self.csv_encoding, newline="") as file:
            csv_writer = csv.writer(file, delimiter=self.csv_separator)
            csv_writer.writerow(
                self.extract_information(prod_fields, ilugg_fields, attribute_names)
            )

    def extract_information(self, prod_fields, ilugg_fields, attribute_names):
        row = []

        # Spezifizierte Felder in row schreiben
        for field_name, value_specification in self.config.items():
            if "iterierbar" in value_specification:
                def get_iterable_value(specification, index):
                    value = None
                    field_name = specification["praefix"] + str(index)
                    if field_name in prod_fields:
                        value = prod_fields[field_name]
                    row.append(value)

                self.__iterate(value_specification, prod_fields, ilugg_fields, get_iterable_value)

            else:
                if field_name in special_cases:
                    parameters = {
                        "prod_fields": prod_fields,
                        "attribute_names": attribute_names,
                        "tooltips": self.tooltips
                    }
                    value = special_cases[field_name](parameters)
                else:
                    value = self.__get_value(value_specification, prod_fields, ilugg_fields)

                row.append(value)

        return row

    def __get_value(self, specification, prod_fields, ilugg_fields):
        if "wert" in specification:
            value = specification["wert"]
        elif "prod" in specification:
            value = None
            if specification["prod"] in prod_fields:
                value = prod_fields[specification["prod"]]
        elif "ilugg" in specification:
            value = None
            if specification["ilugg"] in ilugg_fields:
                value = ilugg_fields[specification["ilugg"]]
        else:
            value = None
        return value

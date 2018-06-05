# -*- coding: utf-8 -*-
import os, json, csv

class ShopExporter:
    def __init__(self, general_config_file, shop_name, manufacturer_ending):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
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

        # Erstelle die CSV Dateien und schreibe die festgelegten Attribute als
        # Header
        for manufacturer_directory in os.listdir(self.bsvp_directory):
            if manufacturer_directory.endswith(self.manufacturer_ending):
                csv_path = self.__csv_path(manufacturer_directory)
                with open(csv_path, "w", encoding=self.csv_encoding, newline="") as file:
                    csv_writer = csv.writer(
                        file,
                        delimiter=self.csv_separator
                    )
                    header_fields = list(self.config.keys())
                    csv_writer.writerow(header_fields)

    def write_to_csv(self, prod_fields, ilugg_fields, manufacturer_directory):
        csv_path = self.__csv_path(manufacturer_directory)
        with open(csv_path, "a", encoding=self.csv_encoding, newline="") as file:
            csv_writer = csv.writer(file, delimiter=self.csv_separator)
            csv_writer.writerow(self.extract_information(prod_fields, ilugg_fields))

    def extract_information(self, prod_fields, ilugg_fields):
        row = []

        # Spezifizierte Felder in row schreiben
        for field_name, value_specification in self.config.items():
            if "wert" in value_specification:
                value = value_specification["wert"]
            elif "prod" in value_specification:
                value = None
                if value_specification["prod"] in prod_fields:
                    value = prod_fields[value_specification["prod"]]
            elif "ilugg" in value_specification:
                value = None
                if value_specification["ilugg"] in ilugg_fields:
                    value = ilugg_fields[value_specification["ilugg"]]
            else:
                # TODO implement other cases
                print("OTHER CASE!")
                value = None
            row.append(value)

        return row

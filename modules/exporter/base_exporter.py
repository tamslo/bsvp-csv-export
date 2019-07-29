import csv
import json
import os
import shutil
from modules.constants import GENERAL_CONFIG_FILE, ARCHIVE_DIRECTORY, \
    CONFIGS_DIRECTORY, DATA_DIRECTORY, TOOLTIP_PATH, EXPORT_DIRECTORY

class BaseExporter:
    def __init__(self, manufacturers):
        with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)
            self.manufacturers = manufacturers
            self.shop_csv_separator = self.config["shop-csv-separator"]
            self.configurator_csv_separator = self.config["konfigurator-csv-separator"]
            self.csv_encoding = self.config["csv-encoding"]
            self.csv_quote_char = self.config["csv-quote-char"]
            self.csv_escpape_char = self.config["csv-escape-char"]
            self.configs_base_directory = CONFIGS_DIRECTORY
            self.bsvp_directory = DATA_DIRECTORY
            self.tooltip_path = TOOLTIP_PATH

            # Standardwerte für Konfiguration des Exporters
            self.uses_manufacturer_information = False
            self.skipping_policy = {
                "manufacturers": True,
                "delivery_status": True
            }

    def name(self):
        raise Exception("BaseExporter::name needs to be implemented by extending classes")

    def output_directory(self):
        return EXPORT_DIRECTORY + self.name() + "/"

    def __archive_base_directory(self):
        return EXPORT_DIRECTORY + ARCHIVE_DIRECTORY + "/"

    def __archive_directory(self):
        return self.__archive_base_directory() + self.name() + "/"

    def skip_manufacturer(self, manufacturer_name, selected_manufacturers):
        return self.skipping_policy["manufacturers"] and not manufacturer_name in selected_manufacturers

    def skip_product(self, fields):
        if not self.skipping_policy["delivery_status"]:
            return False, None

        if not "DELSTAT" in fields:
            return None, "KEIN_DELSTAT"

        delivery_status = fields["DELSTAT"]
        active_delivery_statuses = ["0", "1", "2", "3", "4"]
        return not delivery_status in active_delivery_statuses, None

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
            csv_writer = csv.writer(file, delimiter=self.csv_separator, quotechar=self.csv_quote_char, escapechar=self.csv_escpape_char, quoting=csv.QUOTE_NONE)

            # Remove knwon characters that cause UnicodeEncodeError
            toxic_characters = {
                "∆": "&#8710;",
                "✓": "&checkmark;"
            }
            clean_row = []
            for field in row:
                clean_field = field
                if clean_field != None:
                    for toxic_character, html_escape_code in toxic_characters.items():
                        clean_field = clean_field.replace(toxic_character, html_escape_code)
                clean_row.append(clean_field)

            try:
                csv_writer.writerow(clean_row)
                return None
            except UnicodeEncodeError as error:
                return "FEHLER BEIM SCHREIBEN ({})".format(error)

    def write_to_csv(self, **args):
        raise Exception("BaseExporter::write_to_csv needs to be implemented by extending classes")

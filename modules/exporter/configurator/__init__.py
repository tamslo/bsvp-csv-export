# -*- coding: utf-8 -*-
from ..base_exporter import BaseExporter
from .configs import transform_configs
from .formatter import format_field
from modules.constants import CONFIGURATOR_NAME, PRODUCT_TYPE_ID

class ConfiguratorExporter(BaseExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers)
        self.csv_separator = self.configurator_csv_separator
        self.configs_directory = self.configs_base_directory + self.name() + "/"
        self.export_configs = transform_configs(self.configs_directory, self.output_directory())

        # Konfiguration des Exporters
        self.skipping_policy["manufacturers"] = False

    def name(self):
        return CONFIGURATOR_NAME

    def setup(self):
        super().setup()
        # Erstelle die CSV Dateien und schreibe die festgelegten Attribute als
        # Header
        for config in list(self.export_configs.values()):
            for output in config["outputs"]:
                header_fields = []
                fields = config["felder"]
                for field in list(fields.keys()):
                    field_value = fields[field]
                    if isinstance(field_value, str):
                        header_fields.append(field_value)
                    else:
                        header_fields += list(field_value.values())
                header_fields += list(config["kombinationen"].keys())
                self.write_csv_row(output["path"], header_fields, file_mode="w")

    def write_to_csv(self, parameters):
        fields = parameters["fields"]
        error_code = validate_fields(fields)
        if error_code != None:
            return error_code

        fields = flatten_fields(fields)
        manufacturer = fields["MANUFACTURER"]
        product_type = fields[PRODUCT_TYPE_ID]
        if product_type in self.export_configs:
            config = self.export_configs[product_type]
            error_code = None
            for output in config["outputs"]:
                if output["base"] or output["manufacturer"] == manufacturer:
                    product_information = extract_product_information(config, fields)
                    error_code = self.write_csv_row(output["path"], product_information)
            return error_code

def validate_fields(fields):
    if not "TECHDATA" in fields:
        return "KEIN_TECHDATA"
    if not fields["TECHDATA"]:
        return "TECHDATA_LEER"
    if not PRODUCT_TYPE_ID in fields["TECHDATA"]:
        return "KEIN_PRODUKTTYP"
    return None

# Hilfsmethode, entpackt verschachtelte Felder wie TECHDATA
def flatten_fields(fields):
    flattened_fields = {}
    for field_name, field_value in fields.items():
        if isinstance(field_value, str):
            flattened_fields[field_name] = field_value
        else:
            for attribute_name, attribute_value in field_value.items():
                flattened_fields[attribute_name] = attribute_value
    return flattened_fields

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

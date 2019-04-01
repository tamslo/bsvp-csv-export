# -*- coding: utf-8 -*-
from ..base_exporter import BaseExporter
from .configs import transform_configs
from .formatter import format_field
from modules.constants import CONFIGURATOR_NAME

class ConfiguratorExporter(BaseExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers)
        self.csv_separator = self.configurator_csv_separator
        self.configs_directory = self.configs_base_directory + self.name() + "/"
        self.export_configs = transform_configs(self.configs_directory, self.output_directory())

    def name(self):
        return CONFIGURATOR_NAME

    def should_skip(self, manufacturer_name, selected_manufacturers):
        return False

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
        fields = parameters["flattened_fields"]
        product_type = parameters["product_type"]
        manufacturer = fields["MANUFACTURER"]
        delivery_status = fields["DELSTAT"]
        active_delivery_statuses = ["0", "1", "2", "3", "4"]
        if product_type in self.export_configs and delivery_status in active_delivery_statuses:
            config = self.export_configs[product_type]
            for output in config["outputs"]:
                if output["base"] or output["manufacturer"] == manufacturer:
                    product_information = extract_product_information(config, fields)
                    return self.write_csv_row(output["path"], product_information)

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

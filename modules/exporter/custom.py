import json
from .base_exporter import BaseExporter
from collections import OrderedDict
from modules.constants import CUSTOM_NAME
from modules.exporter.utils.flatten_fields import flatten_fields

class CustomExporter(BaseExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers)
        self.csv_separator = self.configurator_csv_separator
        export_config_path = self.configs_base_directory + self.name() + ".json"
        with open(export_config_path, "r", encoding="utf-8") as export_config_file:
            self.export_config = json.load(export_config_file, object_pairs_hook=OrderedDict)

        self.skipping_policy["manufacturers"] = False
        self.skipping_policy["delivery_status"] = False

    def name(self):
        return CUSTOM_NAME

    def write_to_csv(self, parameters):
        prod_fields = flatten_fields(parameters["fields"])
        manufacturer_name = parameters["manufacturer_name"]
        csv_path = self.output_directory() + "complete.csv"
        header_fields = list(self.export_config.keys())
        self.maybe_create_csv(csv_path, header_fields)
        csv_row = list(map(
            lambda field: prod_fields[field] if field in prod_fields else None,
            list(self.export_config.values())
        ))
        return self.write_csv_row(csv_path, csv_row)

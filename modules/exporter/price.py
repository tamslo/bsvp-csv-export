from .base_exporter import BaseExporter
from collections import OrderedDict

class PriceExporter(BaseExporter):
    def __init__(self, general_config_file, price_name, config):
        super().__init__(general_config_file, price_name)
        self.csv_separator = self.configurator_csv_separator
        self.config = OrderedDict(config)

    def write_to_csv(self, manufacturer_name, prod_fields):
        csv_path = self.output_directory + manufacturer_name + ".csv"
        header_fields = list(self.config.keys())
        self.maybe_create_csv(csv_path, header_fields)
        csv_row = list(map(
            lambda field: prod_fields[field],
            list(self.config.values())
        ))
        self.write_csv_row(csv_path, csv_row)

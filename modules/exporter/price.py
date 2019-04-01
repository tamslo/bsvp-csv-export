from .base_exporter import BaseExporter
from collections import OrderedDict
from modules.constants import PRICE_NAME

class PriceExporter(BaseExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers)
        self.csv_separator = self.configurator_csv_separator
        self.export_config = OrderedDict({
            "artikelnummer": "ARTNR",
            "artikelname": "NAME",
            "listenpreis": "PRICE"
        })

    def name(self):
        return PRICE_NAME

    def write_to_csv(self, parameters):
        prod_fields = parameters["fields"]
        manufacturer_name = parameters["manufacturer_name"]
        csv_path = self.output_directory() + manufacturer_name + ".csv"
        header_fields = list(self.export_config.keys())
        self.maybe_create_csv(csv_path, header_fields)
        csv_row = list(map(
            lambda field: prod_fields[field],
            list(self.export_config.values())
        ))
        return self.write_csv_row(csv_path, csv_row)

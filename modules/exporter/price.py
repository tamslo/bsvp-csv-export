from .base_exporter import BaseExporter
from collections import OrderedDict

class PriceExporter(BaseExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers)
        self.csv_separator = self.configurator_csv_separator
        self.config = OrderedDict({
            "artikelnummer": "ARTNR",
            "artikelname": "NAME",
            "listenpreis": "PRICE"
        })

    def name(self):
        return "Listenpreise"

    def write_to_csv(self, manufacturer_name, prod_fields):
        csv_path = self.output_directory() + manufacturer_name + ".csv"
        header_fields = list(self.config.keys())
        self.maybe_create_csv(csv_path, header_fields)
        csv_row = list(map(
            lambda field: prod_fields[field],
            list(self.config.values())
        ))
        self.write_csv_row(csv_path, csv_row)

from .shop import ShopExporter
from modules.constants import GAMBIO_NAME, SHOP_NAME
from modules.logger import Logger

class GambioExporter(ShopExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers, SHOP_NAME)

        # Konfiguration des Exporters
        self.skipping_policy["delivery_status"] = False

    def name(self):
        return GAMBIO_NAME

    def header_fields(self, prod_fields, ilugg_fields):
        header_fields = super().header_fields(prod_fields, ilugg_fields)
        header_fields.append("Foo")
        return header_fields

    def extract_information(self, prod_fields, ilugg_fields, attribute_names, attribute_types):
        row = super().extract_information(prod_fields, ilugg_fields, attribute_names, attribute_types)
        row.append("Bar")
        return row

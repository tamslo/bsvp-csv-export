from .shop import ShopExporter
from .complete import get_complete_header_fields as get_complete_techdata_fields
from modules.constants import GAMBIO_NAME, SHOP_NAME, TECHDATA
from modules.logger import Logger

class GambioExporter(ShopExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers, SHOP_NAME)
        general_fields, techdata_fields = get_complete_techdata_fields(self.manufacturers)
        self.techdata_fields = techdata_fields

        # Konfiguration des Exporters
        self.skipping_policy["delivery_status"] = False

    def name(self):
        return GAMBIO_NAME

    def header_fields(self, prod_fields, ilugg_fields):
        header_fields = super().header_fields(prod_fields, ilugg_fields)
        header_fields = header_fields + self.techdata_fields
        return header_fields

    def extract_information(self, prod_fields, ilugg_fields, attribute_names, attribute_types):
        row = super().extract_information(prod_fields, ilugg_fields, attribute_names, attribute_types)
        for techdata_field in self.techdata_fields:
            value = None
            if (TECHDATA in prod_fields):
                techdata = prod_fields[TECHDATA]
                if techdata_field in techdata:
                    value = techdata[techdata_field]
            row.append(value)
        return row

from .shop import ShopExporter
from .complete import get_complete_header_fields as get_complete_techdata_fields
from modules.constants import GAMBIO_NAME, SHOP_NAME, TECHDATA

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
        # Fasse Werte von p_cat.x in p_cat.0 zusammen
        # Lasse die übrigen p_cat Felder leer
        header_fields = self.header_fields(prod_fields, ilugg_fields)
        category_prefix = "p_cat."
        main_category = "{}0".format(category_prefix)
        main_category_index = None
        other_category_indices = []
        category_values = []
        current_field_index = 0
        for header_field in header_fields:
            if header_field.startswith(category_prefix):
                category_value = row[current_field_index]
                if category_value != "":
                    category_values.append(category_value)
                if header_field == main_category:
                    main_category_index = current_field_index
                else:
                    other_category_indices.append(current_field_index)
            current_field_index = current_field_index + 1
        row[main_category_index] = " > ".join(category_values)
        for other_category_index in other_category_indices:
            row[other_category_index] = None

        # Füge TECHDATA Felder hinter Shop Feldern an
        for techdata_field in self.techdata_fields:
            value = None
            if TECHDATA in prod_fields:
                techdata = prod_fields[TECHDATA]
                if techdata_field in techdata:
                    value = techdata[techdata_field]
            row.append(value)
        return row

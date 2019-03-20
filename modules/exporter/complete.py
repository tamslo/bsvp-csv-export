import os
from modules.parser.prod import parse_product

def get_complete_header_fields(manufacturers):
    general_fields = set()
    techdata_fields = set()

    for manufacturer_name, manufacturer in manufacturers.items():
        for product_name, product_path in manufacturer["products"].items():
            if os.path.exists(product_path):
                fields, attribute_names, attribute_types = parse_product(product_path)
                for field_name, field_value in fields.items():
                    if field_name != "TECHDATA":
                        general_fields.add(field_name)
                    else:
                        for field_id in field_value.keys():
                            techdata_fields.add(field_id)

    return sorted(general_fields), sorted(techdata_fields)

from .base_exporter import BaseExporter
from collections import OrderedDict

class CompleteExporter(BaseExporter):
    def __init__(self, general_config_file, complete_name, manufacturers):
        super().__init__(general_config_file, complete_name)
        self.csv_separator = self.configurator_csv_separator
        self.general_fields, self.techdata_fields = get_complete_header_fields(manufacturers)

    def __header_fields(self):
        return self.general_fields + list(map(
            lambda field: "TECHDATA.{}".format(field),
            self.techdata_fields
        ))

    def write_to_csv(self, manufacturer_name, prod_fields):
        csv_path = self.output_directory + manufacturer_name + ".csv"
        self.maybe_create_csv(csv_path, self.__header_fields())
        csv_row = list(map(
            lambda field: field in prod_fields and prod_fields[field] or None,
            self.general_fields
        ))
        csv_row += list(map(
            lambda field: field in prod_fields["TECHDATA"] and prod_fields["TECHDATA"][field] or None,
            self.techdata_fields
        ))
        self.write_csv_row(csv_path, csv_row)
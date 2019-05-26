import os
from modules.parser.prod import parse_product
from modules.parser.attributes import parse_attributes
from modules.constants import COMPLETE_NAME
from modules.logger import Logger

def get_complete_header_fields(manufacturers):
    general_fields = set()
    techdata_fields = set()

    for manufacturer_name, manufacturer in manufacturers.items():
        for product_name, product_path in manufacturer["products"].items():
            if os.path.exists(product_path):
                fields, attribute_names, attribute_types, error_code = parse_product(product_path)
                if error_code != None:
                    continue
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
    def __init__(self, manufacturers):
        super().__init__(manufacturers)
        self.csv_separator = self.configurator_csv_separator
        self.general_fields, self.techdata_fields = get_complete_header_fields(manufacturers)

        # Konfiguration des Exporters
        self.skipping_policy["delivery_status"] = False

    def __header_fields(self):
        return self.general_fields + self.techdata_fields

    def name(self):
        return COMPLETE_NAME

    def setup(self):
        super().setup()

        # Sanity checks
        attribute_mapping = parse_attributes()
        logger = Logger()

        logger.log("")
        logger.log("Starte Plausibilitätsprüfung der technischen Datenfelder...")
        logger.log("")

        logger.log("Felder ohne Namen in MasterRecordMask:")
        logger.log("")
        for techdata_field in self.techdata_fields:
            if techdata_field not in attribute_mapping:
                logger.log(techdata_field)

        logger.log("")
        logger.log("Felder die nicht in Produkten genutzt werden:")
        logger.log("")
        for techdata_field, attribute_name in attribute_mapping.items():
            if techdata_field not in self.techdata_fields:
                logger.log("{} ({})".format(attribute_name, techdata_field))

        logger.log("")
        logger.log("Plausibilitätsprüfung der technischen Datenfelder beendet.")
        logger.log("")

    def write_to_csv(self, parameters):
        prod_fields = parameters["fields"]
        manufacturer_name = parameters["manufacturer_name"]
        csv_path = self.output_directory() + manufacturer_name + ".csv"
        self.maybe_create_csv(csv_path, self.__header_fields())
        csv_row = list(map(
            lambda field: field in prod_fields and prod_fields[field] or None,
            self.general_fields
        ))
        csv_row += list(map(
            lambda field: "TECHDATA" in prod_fields and field in prod_fields["TECHDATA"] and prod_fields["TECHDATA"][field] or None,
            self.techdata_fields
        ))
        return self.write_csv_row(csv_path, csv_row)

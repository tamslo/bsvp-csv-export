import math
import re
from .configurator import ConfiguratorExporter
from modules.constants import PRESTA_NAME, ARTICLE_NUMBER, WIDTH, DEPTH, HEIGHT
from modules.logger import Logger

class PrestaExporter(ConfiguratorExporter):
    def name(self):
        return PRESTA_NAME

    def header_fields(self, config):
        header_fields = ["Artikelnummer", "Eigenschaften", "Breite", "Tiefe", "Höhe"]
        return header_fields

    def export_fields(self, config, fields):
        product_information = {}
        outside_fields = [ARTICLE_NUMBER, WIDTH, DEPTH, HEIGHT]
        for field_name, field_value in config["felder"].items():
            if not field_name in outside_fields:
                product_information[field_value] = self.get_field(config, fields, field_name)
        return product_information

    def export_kombinations(self, config, fields):
        product_information = {}
        for name, combination in config["kombinationen"].items():
            product_information[name] = self.export_kombination(config, fields, combination)
        return product_information

    def combine_product_information(self, information, other_information):
        return {**information, **other_information}

    def build_properties(self, config, fields):
        property_separator = ", "
        value_separator = ":"
        properties = []
        product_information = super().extract_product_information(config, fields)
        logger = Logger()
        for field_name, field_value in product_information.items():
            if field_value == None:
                field_value = ""
                log_message = "Fehlender Wert für {} in {}".format(field_name, fields[ARTICLE_NUMBER])
                logger.log(log_message)
            properties.append(field_name + value_separator + field_value)
        return property_separator.join(properties)

    def extract_product_information(self, config, fields):
        product_information = []
        product_information.append(self.get_field(config, fields, ARTICLE_NUMBER))
        product_information.append(self.build_properties(config, fields))
        for measure in [WIDTH, DEPTH, HEIGHT]:
            product_information.append(self.get_field(config, fields, measure))
        return product_information

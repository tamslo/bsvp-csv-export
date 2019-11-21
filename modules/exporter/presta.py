from .configurator import ConfiguratorExporter
from modules.constants import PRESTA_NAME

class PrestaExporter(ConfiguratorExporter):
    def name(self):
        return PRESTA_NAME

    def header_fields(self, config):
        # TODO: Adapt for Presta shop
        header_fields = []
        fields = config["felder"]
        for field in list(fields.keys()):
            field_value = fields[field]
            if isinstance(field_value, str):
                header_fields.append(field_value)
            else:
                header_fields += list(field_value.values())
        header_fields += list(config["kombinationen"].keys())
        return header_fields

    def extract_product_information(self, config, fields):
        # TODO: Adapt for Presta shop
        # TODO: ART_NR, Eigenschaften, Breite, Höhe, Tiefe
        # TODO: Breite, Höhe, Tiefe aufrunden
        product_information = []

        # Spezifizierte Felder in product_information schreiben
        for field_name, field_value in config["felder"].items():
            product_information.append(self.get_field(config, fields, field_name))

        # Spezifizierte Kominationen bilden und in product_information schreiben
        for name, combination in config["kombinationen"].items():
            fields = list(map(
                lambda field_name: self.get_field(config, fields, field_name) or "",
                combination["felder"]
            ))
            if all(field == "" for field in fields):
                product_information.append(None)
            else:
                product_information.append(combination["separator"].join(fields))

        return product_information

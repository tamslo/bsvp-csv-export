# -*- coding: utf-8 -*-
from modules.constants import MANUFACTURER_ENDING, SHOP_NAME
from ..base_exporter import BaseExporter
import json
from modules.parser.tooltips import parse_tooltips
from .description import export_description
from .energy_efficiency_text import export_energy_efficiency_text
from .video import export_video
from modules.exporter.utils.unescape_bsvp import unescape_bsvp_to_html
from collections import OrderedDict

special_cases = {
    "p_desc.de": export_description,
    "products_energy_efficiency_text": export_energy_efficiency_text,
    "p_movies.de": export_video
}

def special_case_names():
    return list(special_cases.keys())

def escape(value):
    if value == None:
        return None
    return unescape_bsvp_to_html(value)

class ShopExporter(BaseExporter):
    def __init__(self, manufacturers):
        super().__init__(manufacturers)
        self.manufacturer_ending = MANUFACTURER_ENDING
        self.tooltips = parse_tooltips(self.tooltip_path)
        self.csv_separator = self.shop_csv_separator
        export_config_path = self.configs_base_directory + self.name() + ".json"
        with open(export_config_path, "r", encoding="utf-8") as export_config_file:
            self.export_config = json.load(export_config_file, object_pairs_hook=OrderedDict)

        # Konfiguration des Exporters
        self.uses_manufacturer_information = True

    def name(self):
        return SHOP_NAME

    def __csv_path(self, manufacturer_name):
        return self.output_directory() + manufacturer_name + ".csv"

    def __header_fields(self, prod_fields, ilugg_fields):
        header_fields = []
        for field_name, value_specification in self.export_config.items():
            if "iterierbar" in value_specification:
                def make_header_field(specification, index):
                    header_fields.append(field_name + str(index))
                self.__iterate(value_specification, prod_fields, ilugg_fields, make_header_field)
            else:
                header_fields.append(field_name)

        return header_fields

    def __iterate(self, value_specification, prod_fields, ilugg_fields, callback):
        specification = value_specification["iterierbar"]
        max = int(self.__get_value(
            specification["max"],
            prod_fields,
            ilugg_fields
        ))
        start = 0 if not "start" in specification else int(specification["start"])
        while start < max:
            callback(specification, start)
            start += 1

    def write_to_csv(self, parameters):
        prod_fields = parameters["fields"]
        attribute_names = parameters["attribute_names"]
        attribute_types = parameters["attribute_types"]
        ilugg_fields = parameters["manufacturer_information"]
        manufacturer_name = parameters["manufacturer_name"]

        has_exportflag = "EXPORTFLAG" in prod_fields
        if has_exportflag:
            export_flag = prod_fields["EXPORTFLAG"]
            exportable_flags = ["export", "explicit"]
            if not export_flag in exportable_flags:
                return "EXPORTFLAG = {}".format(export_flag)

        csv_path = self.__csv_path(manufacturer_name)
        self.maybe_create_csv(csv_path, self.__header_fields(prod_fields, ilugg_fields))
        row = self.extract_information(prod_fields, ilugg_fields, attribute_names, attribute_types)
        row = map(escape, row)
        write_error_code =  self.write_csv_row(csv_path, row)
        if write_error_code == None and not has_exportflag:
            return "KEIN EXPORTFLAG (trotzdem in Export enthalten)"
        else:
            return write_error_code # könnte ein Fehler oder None sein, wenn alles funktioniert hat

    def extract_information(self, prod_fields, ilugg_fields, attribute_names, attribute_types):
        row = []

        # Spezifizierte Felder in row schreiben
        for field_name, value_specification in self.export_config.items():
            if "iterierbar" in value_specification:
                def get_iterable_value(specification, index):
                    value = None
                    field_name = specification["praefix"] + str(index)
                    if field_name in prod_fields:
                        value = prod_fields[field_name]
                    row.append(value)

                self.__iterate(value_specification, prod_fields, ilugg_fields, get_iterable_value)

            else:
                if field_name in special_cases:
                    parameters = {
                        "prod_fields": prod_fields,
                        "ilugg_fields": ilugg_fields,
                        "attribute_names": attribute_names,
                        "attribute_types": attribute_types,
                        "tooltips": self.tooltips,
                        "specification": value_specification
                    }
                    value = special_cases[field_name](parameters)
                else:
                    value = self.__get_value(value_specification, prod_fields, ilugg_fields)

                row.append(value)

        return row

    def __get_value(self, specification, prod_fields, ilugg_fields):
        value = None
        if "wert" in specification:
            value = specification["wert"]
        elif "prod" in specification:
            prod_field = specification["prod"]
            if prod_field in prod_fields:
                value = prod_fields[prod_field]
                # Wenn das Feld ein Preisfeld ist, den Separator entfernen, damit der Shop das Komma
                # nicht beim Separator setzt
                if "PRICE" in prod_field and "," in value:
                    value = value.replace(".", "")
                    value = value.replace(",", ".")
        elif "ilugg" in specification:
            ilugg_field = specification["ilugg"]
            if ilugg_field in ilugg_fields:
                value = ilugg_fields[ilugg_field]
        return value

# -*- coding: utf-8 -*-
import os, json
from collections import OrderedDict

def replace(value, prior, afterwards):
    if value.lower() == prior.lower():
        return afterwards
    else:
        return value

def format_boolean(value):
    value = replace(value, "ja", "yes")
    value = replace(value, "nein", "no")
    return value

def format_integrated(value):
    return replace(value, "vorhanden", "integriert")

def format_decimal_separator(value):
    return value.replace('.',',')

def format_cooling(value):
    return replace(value, "stille Kühlung", "statische Kühlung")

def format_pluggable(value):
    return replace(value, "ja", "steckerfertig")

def format_voltage(value):
    print(replace(value, "220 - 240 Volt", "230 Volt"))
    return replace(value, "220 - 240 Volt", "230 Volt")

def range_from_zero(value):
    try:
        float(value)
    except:
        pass
    return "0|" + value

formatters = {
    "wahrheitswert_englisch": format_boolean,
    "vorhanden_zu_integriert": format_integrated,
    "punkt_zu_komma": format_decimal_separator,
    "stille_kühlung_zu_statische_kühlung": format_cooling,
    "ja_zu_steckfertig": format_pluggable,
    "bereich_von_null": range_from_zero,
    "230_volt": format_voltage
}

def format_rules():
    return list(formatters.keys())

class Formatter:
    def __init__(self, general_config_file):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.configs_directory = general_config["configs_directory"]
            self.format_options = self.__transform_configs()

    def __transform_configs(self):
        format_options = {}
        for config_name in os.listdir(self.configs_directory):
            if config_name.endswith(".json"):
                product_type, options = self.__transform_config(config_name)
                format_options[product_type] = options
        return format_options

    def __transform_config(self, config_name):
        config_path = self.configs_directory + config_name
        with open(config_path, "r",  encoding="utf-8") as config_file:
            config = json.load(config_file, object_pairs_hook=OrderedDict)
            format_options = {}
            if "formatierungen" in config:
                for option in config["formatierungen"]:
                    for field in config["formatierungen"][option]:
                        format_options[field] = option
            return config["produkttyp"], format_options

    def format(self, fields, product_type_id):
        product_type = fields["TECHDATA"][product_type_id]
        if product_type in self.format_options:
            formatted_fields = {}
            format_options = self.format_options[product_type]
            for field_name in fields:
                field_value = fields[field_name]
                if isinstance(field_value, str):
                    formatted_fields[field_name] = format_value(
                        field_name,
                        field_value,
                        format_options
                    )
                else:
                    formatted_fields[field_name] = {}
                    for attribute_name, attribute_value in field_value.items():
                        formatted_fields[field_name][attribute_name] = format_value(
                            attribute_name,
                            attribute_value,
                            format_options
                        )
            return formatted_fields
        else:
            return fields

def format_value(name, value, format_options):
    if name in format_options:
        return formatters[format_options[name]](value)
    else:
        return value

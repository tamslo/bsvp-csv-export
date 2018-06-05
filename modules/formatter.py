# -*- coding: utf-8 -*-
import os, json
from collections import OrderedDict

def format_decimal_separator(value):
    return value.replace('.',',')

def range_from_zero(value):
    try:
        float(value)
    except:
        pass
    return "0|" + value

formatters = {
    "punkt_zu_komma": format_decimal_separator,
    "bereich_von_null": range_from_zero,
    "ersetzungen": None
}

def format_rules():
    return list(formatters.keys())

class Formatter:
    def __init__(self, general_config_file):
        with open(general_config_file, "r", encoding="utf-8") as config_file:
            general_config = json.load(config_file)
            self.configs_directory = general_config["configs-ordner"] + "Konfigurator/"
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
                    if option == "ersetzungen":
                        for ersetzung in config["formatierungen"][option]:
                            for field in ersetzung["felder"]:
                                option = {
                                    "type": "ersetzung",
                                    "before": ersetzung["vorher"],
                                    "afterwards": ersetzung["nachher"]
                                }
                                add_format_option(format_options, field, option)
                    else:
                        for field in config["formatierungen"][option]:
                            option = { "type": option }
                            add_format_option(format_options, field, option)
            return config["produkttyp"], format_options

    def format(self, fields, product_type_id):
        product_type = fields[product_type_id]
        if product_type in self.format_options:
            formatted_fields = {}
            format_options = self.format_options[product_type]
            for field_name, field_value in fields.items():
                formatted_fields[field_name] = format_value(
                    field_name,
                    field_value,
                    format_options
                )
            return formatted_fields
        else:
            return fields

def add_format_option(format_options, field, option):
    if field in format_options:
        format_options[field].append(option)
    else:
        format_options[field] = [option]

def format_value(field, value, format_options):
    if field in format_options:
        for format_option in format_options[field]:
            if format_option["type"] == "ersetzung":
                before_values = list(map(
                    lambda value: value.lower(),
                    format_option["before"]
                ))
                if value.lower() in before_values:
                    value = format_option["afterwards"]
            else:
                value = formatters[format_option["type"]](value)
    return value

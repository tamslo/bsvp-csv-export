# -*- coding: utf-8 -*-
import os, yaml
from collections import OrderedDict
from modules.constants import CONFIGS_DIRECTORY, FORMATTING_CONFIG_FILE
from .decimal_separator import decimal_separator
from .range_from_zero import range_from_zero
from .replacement import replacement
from .grouping import grouping

formatters = {
    "punkt_zu_komma": decimal_separator,
    "bereich_von_null": range_from_zero,
    "ersetzungen": replacement,
    "gruppierungen": grouping
}

def get_format_options():
    with open(os.path.join(CONFIGS_DIRECTORY, FORMATTING_CONFIG_FILE), "r") as formatting_config_file:
        format_config = yaml.load(formatting_config_file, Loader=yaml.FullLoader)
    
    # Formatierungen so umschreiben, dass sie durch die Feld ID erreichbar sind.
    # Für jedes Feld wird eine Liste von Formatierungen angegeben.
    # Wenn Reihenfolgen angegeben sind, werden diese Listen so sortiert, dass
    # zuerst die Formatierungen mit spezifizierter Reihenfolge bearbeitet werden.
    
    format_options = {}

    def add_format_option(format_options, field, option):
        if field in format_options:
            format_options[field].append(option)
        else:
            format_options[field] = [option]

    for option in format_config:
        if option == "ersetzungen" or option == "gruppierungen":
            for parameters in format_config[option]:
                for field in parameters["felder"]:
                    format_option = { "type": option }
                    if "id" in parameters:
                        format_option["id"] = parameters["id"]
                    if option == "ersetzungen":
                        format_option["before"] = parameters["vorher"]
                        format_option["afterwards"] = parameters["nachher"]
                        format_option["option"] = "option" in parameters and parameters["option"] or None
                    else: # option == "gruppierungen":
                        format_option["thresholds"] = parameters["grenzwerte"]
                        format_option["unit"] = parameters["einheit"]
                    add_format_option(format_options, field, format_option)

    def sort_format_options(format_config, format_options):
        for ordering in format_config["reihenfolgen"]:
            formatter_ordering = ordering["reihenfolge"]
            for field in ordering["felder"]:
                if field in format_options:
                    field_options = format_options[field]
                    ordered_field_options = []
                    covered_indices = []
                    for formatter_position in formatter_ordering:
                        field_option_index = next((index
                            for (index, field_option) in enumerate(field_options)
                            if "id" in field_option and field_option["id"] == formatter_position), None)
                        if field_option_index != None:
                            field_option = field_options[field_option_index]
                            ordered_field_options.append(field_option)
                            covered_indices.append(field_option_index)
                    for index, field_option in enumerate(field_options):
                        if not index in covered_indices:
                            ordered_field_options.append(field_option)
                    format_options[field] = ordered_field_options
        return format_options

    if "reihenfolgen" in format_config:
        format_options = sort_format_options(format_config, format_options)

    return(format_options)

format_options = get_format_options()

def format_field(value, field_name):
    if field_name in format_options:
        for format_option in format_options[field_name]:
            value = formatters[format_option["type"]](value, format_option)
    return value
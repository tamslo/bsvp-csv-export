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
    "ersetzungen": None # für die Validierung der Export-Konfigurationen
}

def format_rules():
    return list(formatters.keys())

def format_field(format_options, value, field_name):
    if field_name in format_options:
        for format_option in format_options[field_name]:
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

# -*- coding: utf-8 -*-
import os, json
from collections import OrderedDict
from modules.logger import Logger

logger = Logger()

def format_decimal_separator(value, format_option):
    return value.replace('.',',')

def range_from_zero(value, format_option):
    try:
        float(value)
    except:
        pass
    return "0|" + value

def replacement(value, format_option):
    before_values = format_option["before"]
    afterwards_value = format_option["afterwards"]
    option = format_option["option"]
    if option == "startswith":
        for before_value in before_values:
            if value.startswith(before_value):
                value = value.replace(before_value, afterwards_value)
                break
    elif option == "endswith":
        for before_value in before_values:
            if value.endswith(before_value):
                value = value.replace(before_value, afterwards_value)
                break
    else:
        lower_before_values = list(map(
            lambda value: value.lower(),
            before_values
        ))
        if value.lower() in lower_before_values:
            value = afterwards_value
    return value

def grouping(value, format_option):
    try:
        numeric_value = float(value.replace(",", "."))
        matching_threshold = None
        for threshold in format_option["thresholds"]:
            if numeric_value <= threshold:
                matching_threshold = threshold
                break

        if matching_threshold != None:
             indicator = "bis"
        else:
            indicator = ">"
            last_threshold = format_option["thresholds"][-1]
            matching_threshold = last_threshold

        unit = format_option["unit"]
        return "{} {}{}".format(indicator, str(matching_threshold), unit)
    except:
        logger.log("Der Wert '{}' kann nicht gruppiert werden, da er nicht numerisch ist.".format(value))
        return value

formatters = {
    "punkt_zu_komma": format_decimal_separator,
    "bereich_von_null": range_from_zero,
    "ersetzungen": replacement,
    "gruppierungen": grouping
}

def format_rules():
    return list(formatters.keys())

def format_field(format_options, value, field_name):
    if field_name in format_options:
        for format_option in format_options[field_name]:
            value = formatters[format_option["type"]](value, format_option)
    return value

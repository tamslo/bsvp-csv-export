# -*- coding: utf-8 -*-
import os, sys, html, re

ARTNR_PREFIX = "§+§ARTNR="
TECH_DATA_PREFIX = "§+§TECHDATA="
DATA_SEPARTOR = "§+§"
ATTRIBUTE_SEPARATOR = "§-§"
INNER_SEPARATOR = "::"

def parse_product(product_path):
    if not os.path.exists(product_path):
        error_code = "PROD_UNTERSCHIEDLICH"
        return None, error_code

    bsvp_file = open(product_path, "r",  encoding="utf-8", errors="ignore")
    product_data = ""
    lines = bsvp_file.readlines()
    bsvp_file.close()

    for line in lines:
        product_data += line

    fields = {}

    for field in product_data.split(DATA_SEPARTOR):
        field_parts = field.split("=")
        if len(field_parts) == 1:
            continue

        field_name = field_parts[0]
        field_value = field_parts[1]
        field_attributes = field_value.split(ATTRIBUTE_SEPARATOR)

        if len(field_attributes) > 1:
            attributes = {}
            for attribute in field_attributes:
                attribute = attribute.split("@")
                if len(attribute) != 2:
                    continue
                try:
                    attribute_id = re.search("\[\[.*\.(.+?)\]\]", attribute[1]).group(1)
                except AttributeError:
                    continue
                try:
                    attribute_value = attribute[0].split("::")[2]
                    if attribute_value == " ":
                        continue
                except IndexError:
                    continue
                attributes[attribute_id] = html.unescape(attribute_value)
            fields[field_name] = attributes
        else:
            fields[field_name] = html.unescape(field_value)

    return fields

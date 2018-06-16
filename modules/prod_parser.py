# -*- coding: utf-8 -*-
import os, sys, html, re

DATA_SEPARTOR = "§+§"
ATTRIBUTE_SEPARATOR = "§-§"

def parse_product(product_path):
    bsvp_file = open(product_path, "r",  encoding="utf-8", errors="ignore")
    lines = bsvp_file.readlines()
    bsvp_file.close()

    product_data = ""
    for line in lines:
        product_data += line

    fields = {}

    for field in product_data.split(DATA_SEPARTOR):
        field_parts = field.split("=", 1)
        if len(field_parts) == 1:
            continue

        field_name = field_parts[0]
        field_value = html.unescape(field_parts[1]).strip()
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
                    attribute_value = html.unescape(attribute[0].split("::")[2]).strip()
                    if attribute_value.strip() == "":
                        continue
                except IndexError:
                    continue
                attributes[attribute_id] = attribute_value
            fields[field_name] = attributes
        else:
            fields[field_name] = field_value

    return fields
# -*- coding: utf-8 -*-
import os, sys, html

TECH_DATA_PREFIX = "§+§TECHDATA="
TECH_DATA_POSTFIX = "§+§"
FIELD_SEPARATOR = "§-§"
INNER_SEPARATOR = "::"

def parse_product(product_path):
    if not os.path.exists(product_path):
        error_code = 901
        return None, error_code

    bsvp_file = open(product_path, encoding="utf-8")
    product_data = ""
    for line in bsvp_file.readlines():
        product_data += line

    tech_data_start = product_data.find(TECH_DATA_PREFIX)
    if tech_data_start == -1:
        error_code = 902
        return None, error_code

    # TECHDATA extrahieren
    product_data = product_data[tech_data_start  + len(TECH_DATA_PREFIX):]
    tech_data_end = product_data.find(TECH_DATA_POSTFIX)
    product_data = product_data[:tech_data_end]

    # Felder auslesen
    fields = {}
    raw_fields = list(filter(lambda field: field != "", product_data.split(FIELD_SEPARATOR)))
    for field in raw_fields:
        parts = field.split(INNER_SEPARATOR);

        # ASSUMPTION TEST
        if len(parts) != 3 and len(parts) != 4:
            print("[WARNING]: Wrong assumption of parts of field made", end="\n")
            print(raw_fields)

        field_name = html.unescape(parts[1])
        field_value = html.unescape(parts[2]) if len(parts) == 4 else None
        fields[field_name] = field_value

    if not "Produkttyp" in fields:
        error_code = 903
        return None, error_code

    return fields, None

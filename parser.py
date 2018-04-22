# -*- coding: utf-8 -*-
import os, sys, html

TECH_DATA_PREFIX = "§+§TECHDATA="
TECH_DATA_POSTFIX = "§+§"
FIELD_SEPARATOR = "§-§"
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

    tech_data_start = product_data.find(TECH_DATA_PREFIX)
    if tech_data_start == -1:
        error_code = "KEIN_TECHDATA"
        return None, error_code

    # TECHDATA extrahieren
    product_data = product_data[tech_data_start  + len(TECH_DATA_PREFIX):]
    tech_data_end = product_data.find(TECH_DATA_POSTFIX)
    product_data = product_data[:tech_data_end]

    # Felder auslesen
    fields = {}
    raw_fields = list(filter(lambda field: field != "", product_data.split(FIELD_SEPARATOR)))
    for field in raw_fields:
        # TODO hier muss noch viel in die Daten geguckt werden
        parts = field.split(INNER_SEPARATOR)
        if len(parts) < 2:
            continue
        field_name = html.unescape(parts[1])
        if len(parts) == 4:
            field_value = html.unescape(parts[2])
        else:
            field_value = None
        fields[field_name] = field_value

    if not "Produkttyp" in fields or fields["Produkttyp"] == None:
        error_code = "KEIN_PRODUKTTYP"
        return None, error_code

    return fields, None

# -*- coding: utf-8 -*-
import os, sys

DATA_SEPARTOR = ";"

def parse_manufacturer_information(ilugg_path):
    fields = {}
    ilugg_file = open(ilugg_path, "r",  encoding="utf-8", errors="ignore")
    lines = ilugg_file.readlines()
    ilugg_file.close()

    manufacturer_data = ""
    for line in lines:
        manufacturer_data += line

    for field in manufacturer_data.split(DATA_SEPARTOR):
        if field != "":
            field_parts = field.split("=")
            field_name = field_parts[0]
            field_value = field_parts[1]
            fields[field_name] = field_value

    return fields

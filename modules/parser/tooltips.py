# -*- coding: utf-8 -*-
import os, sys

DATA_SEPARTOR = ";"

def parse_tooltips(tooltip_path):
    fields = {}
    tooltip_file = open(tooltip_path, "r",  encoding="utf-8", errors="ignore")
    lines = tooltip_file.readlines()
    tooltip_file.close()

    tooltip_data = ""
    for line in lines:
        tooltip_data += line

    for field in tooltip_data.split(DATA_SEPARTOR):
        if field != "":
            tooltip_parts = field.split("::")
            tooltip_key = tooltip_parts[1]
            tooltip_value = tooltip_parts[2]
            fields[tooltip_key] = tooltip_value

    return fields

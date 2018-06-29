# -*- coding: utf-8 -*-
import os, sys

DATA_SEPARTOR = ";"

def parse_manufacturer_information(manufacturer_path, manufacturer_info_ending):
    fields = {}
    ilugg_files = [path for path in os.listdir(manufacturer_path) if path.endswith(manufacturer_info_ending)]
    if len(ilugg_files) < 1:
        return fields

    ilugg_file = ilugg_files[0]
    if len(ilugg_files) > 1:
        print(
            "[WARNUNG] Mehrere .ilugg Dateien in {}, fahre fort mit {}"
            .format(manufacturer_path, ilugg_file)
        )

    ilugg_path = manufacturer_path + "/" + ilugg_file
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

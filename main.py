# -*- coding: utf-8 -*-
import time, json, os
from modules.logger import Logger
from modules.validator import validate_setup, validate_fields
from modules.parser import parse_product
from modules.exporter import Exporter
from modules.formatter import Formatter

# Definition von Konstanten wie Verzeichnissen und Dateiendungen
GENERAL_CONFIG_FILE = "config.json"
MANUFACTURER_ENDING = ".lugg"
PRODUCT_ENDING = ".prod"
PRODUCT_TYPE_ID = "0000191"

logger = Logger(MANUFACTURER_ENDING, PRODUCT_ENDING)
logger.print_start_time()

validate_setup(GENERAL_CONFIG_FILE)
exporter = Exporter(GENERAL_CONFIG_FILE)
formatter = Formatter(GENERAL_CONFIG_FILE)

# Entpackt verschachtelte Felder wie TECHDATA
def flatten_fields(fields):
    flattened_fields = {}
    for field_name, field_value in fields.items():
        if isinstance(field_value, str):
            flattened_fields[field_name] = field_value
        else:
            for attribute_name, attribute_value in field_value.items():
                flattened_fields[attribute_name] = attribute_value
    return flattened_fields

with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
    bsvp_directory = config["bsvp-ordner"]
    for manufacturer_directory in os.listdir(bsvp_directory):
        if manufacturer_directory.endswith(MANUFACTURER_ENDING):
            manufacturer_path = bsvp_directory + manufacturer_directory
            logger.set_manufacturer(manufacturer_directory)
            for product_directory in os.listdir(manufacturer_path):
                if product_directory.endswith(PRODUCT_ENDING):
                    logger.print_manufacturer_progress()
                    product_path = "/".join([
                        manufacturer_path,
                        product_directory,
                        product_directory
                    ])
                    if os.path.exists(product_path):
                        fields = parse_product(product_path)
                        error_code = validate_fields(fields, PRODUCT_TYPE_ID)
                        if error_code == None:
                            flattened_fields = flatten_fields(fields)
                            formatted_fields = formatter.format(flattened_fields, PRODUCT_TYPE_ID)
                            exporter.write_to_csv(formatted_fields, PRODUCT_TYPE_ID)
                        else:
                            logger.log_skip(product_directory, error_code)
                    else:
                        error_code = "PROD_UNTERSCHIEDLICH"
                        logger.log_skip(product_directory, error_code)
            logger.print_manufacturer_summary()

logger.print_end_time()

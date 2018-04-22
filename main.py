# -*- coding: utf-8 -*-
import time, json, os
from validator import validate_setup, validate_fields
from exporter import Exporter
from bsvp_parser import parse_product
from logger import Logger

# Definition von Konstanten wie Verzeichnissen und Dateiendungen
GENERAL_CONFIG_FILE = "config.json"
EXPORT_CONFIGS_DIRECTORY = "configs/"
MANUFACTURER_ENDING = ".lugg"
PRODUCT_ENDING = ".prod"
SKIP_LOG_FILE = "skip.log"
PRODUCT_TYPE_ID = "0000191"

logger = Logger(SKIP_LOG_FILE, MANUFACTURER_ENDING, PRODUCT_ENDING)
exporter = Exporter(GENERAL_CONFIG_FILE, EXPORT_CONFIGS_DIRECTORY)

logger.print_start_time()
validate_setup(GENERAL_CONFIG_FILE, EXPORT_CONFIGS_DIRECTORY)
exporter.prepare_export()

# BSVP Dateien parsen und in CSV Dateien schreiben

with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
    bsvp_data_directory = config["bsvp_data_directory"]
    for manufacturer_directory in os.listdir(bsvp_data_directory):
        if manufacturer_directory.endswith(MANUFACTURER_ENDING):
            manufacturer_path = bsvp_data_directory + manufacturer_directory
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
                            exporter.write_to_csv(fields, PRODUCT_TYPE_ID)
                        else:
                            logger.log_skip(product_directory, error_code)
                    else:
                        error_code = "PROD_UNTERSCHIEDLICH"
                        logger.log_skip(product_directory, error_code)
            logger.print_manufacturer_summary()

logger.print_end_time()

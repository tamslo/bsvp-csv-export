# -*- coding: utf-8 -*-
import time, json, os
from modules.logger import Logger
from modules.validator import validate_setup, validate_fields
from modules.archiver import archive_exports
from modules.parser.prod import parse_product
from modules.parser.ilugg import parse_manufacturer_information
from modules.exporter.configurator import ConfiguratorExporter
from modules.exporter.shop import ShopExporter

# Definition von Konstanten wie Verzeichnissen und Dateiendungen
GENERAL_CONFIG_FILE = "config.json"
MANUFACTURER_ENDING = ".lugg"
MANUFACTURER_INFO_ENDING = ".ilugg"
PRODUCT_ENDING = ".prod"
PRODUCT_TYPE_ID = "0000191"

CONFIGURATOR_NAME = "Konfigurator"
SHOP_NAME = "Shop"

logger = Logger(MANUFACTURER_ENDING, PRODUCT_ENDING)
logger.print_start_time()

validate_setup(GENERAL_CONFIG_FILE, CONFIGURATOR_NAME, SHOP_NAME)
archive_exports(GENERAL_CONFIG_FILE)
configurator_exporter = ConfiguratorExporter(GENERAL_CONFIG_FILE, CONFIGURATOR_NAME)
shop_exporter = ShopExporter(GENERAL_CONFIG_FILE, SHOP_NAME, MANUFACTURER_ENDING)

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
            manufacturer_information = parse_manufacturer_information(
                manufacturer_path,
                MANUFACTURER_INFO_ENDING
            )
            if not manufacturer_information:
                logger.log_skip("ILUGG", "NICHT_AUSWERTBAR")
            for product_directory in os.listdir(manufacturer_path):
                if product_directory.endswith(PRODUCT_ENDING):
                    logger.print_manufacturer_progress()
                    product_path = "/".join([
                        manufacturer_path,
                        product_directory,
                        product_directory
                    ])
                    if os.path.exists(product_path):
                        fields, attribute_names = parse_product(product_path)
                        error_code = validate_fields(fields, PRODUCT_TYPE_ID)
                        if error_code == None:
                            flattened_fields = flatten_fields(fields)
                            product_type = flattened_fields[PRODUCT_TYPE_ID]
                            configurator_exporter.write_to_csv(flattened_fields, product_type)
                            shop_exporter.write_to_csv(
                                flattened_fields,
                                attribute_names,
                                manufacturer_information,
                                manufacturer_directory
                            )
                        else:
                            logger.log_skip(product_directory, error_code)
                    else:
                        error_code = "PROD_UNTERSCHIEDLICH"
                        logger.log_skip(product_directory, error_code)
            logger.print_manufacturer_summary()

logger.print_end_time()

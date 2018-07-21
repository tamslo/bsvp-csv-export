# -*- coding: utf-8 -*-
import time, json, os, argparse
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

# Kommandozeilen-Argumente definieren und auslesen

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--configurator",
    help="nur den Konfigurator Export starten",
    action="store_true"
)
parser.add_argument(
    "-s", "--shop",
    help="nur den Shop Export starten - wenn Hersteller Ordner angegeben werden, werden nur diese exportiert",
    nargs="*",
    metavar="hersteller",
    default=None
)

args = parser.parse_args()
do_configurator_export = args.configurator
do_shop_export = args.shop != None
# Wenn Hersteller-Ordner angegeben sind, ist limited_manufacturers eine Liste,
# sonst False
limited_manufacturers = isinstance(args.shop, list) and len(args.shop) > 0 and args.shop

# Wenn kein Parameter angegeben ist, dann wird alles exportiert
if not do_configurator_export and not do_shop_export:
    do_configurator_export = True
    do_shop_export = True

# Start des eigentlichen Skripts

logger = Logger(PRODUCT_ENDING)
logger.print_start_time()

validate_setup(GENERAL_CONFIG_FILE, CONFIGURATOR_NAME, SHOP_NAME)
archive_exports(GENERAL_CONFIG_FILE)
if do_configurator_export:
    configurator_exporter = ConfiguratorExporter(GENERAL_CONFIG_FILE, CONFIGURATOR_NAME)
if do_shop_export:
    shop_exporter = ShopExporter(GENERAL_CONFIG_FILE, SHOP_NAME, MANUFACTURER_ENDING)

# Hilfsmethode, entpackt verschachtelte Felder wie TECHDATA
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
            manufacturer_name = manufacturer_directory.split(MANUFACTURER_ENDING)[0]

            # Die Hersteller Informationen werden nur für den Shop-Export benötigt
            if do_shop_export:
                ilugg_path = manufacturer_path + "/" + manufacturer_name + MANUFACTURER_INFO_ENDING
                if not os.path.exists(ilugg_path):
                    logger.log_skip("ILUGG", "NICHT_VORHANDEN")
                    continue
                manufacturer_information = parse_manufacturer_information(ilugg_path)
                if not manufacturer_information:
                    logger.log_skip("ILUGG", "NICHT_AUSWERTBAR")
                    continue

            # Wenn nur ein Shop-Export durchgeführt werden soll und nur für
            # bestimmte Hersteller, wird hier überprüft, ob der aktuelle
            # Hersteller exportiert werden soll
            if not do_configurator_export and limited_manufacturers and not manufacturer_name in limited_manufacturers:
                continue

            logger.set_manufacturer(manufacturer_name)

            for product_directory in os.listdir(manufacturer_path):
                if product_directory.endswith(PRODUCT_ENDING):
                    logger.print_manufacturer_progress()
                    product_path = "/".join([
                        manufacturer_path,
                        product_directory,
                        product_directory
                    ])
                    if os.path.exists(product_path):
                        fields, attribute_names, attribute_types = parse_product(product_path)
                        error_code = validate_fields(fields, PRODUCT_TYPE_ID)
                        if error_code == None:
                            if do_configurator_export:
                                flattened_fields = flatten_fields(fields)
                                product_type = flattened_fields[PRODUCT_TYPE_ID]
                                configurator_exporter.write_to_csv(flattened_fields, product_type)

                            if do_shop_export:
                                error_code = shop_exporter.write_to_csv(
                                    fields,
                                    attribute_names,
                                    attribute_types,
                                    manufacturer_information,
                                    manufacturer_directory
                                )
                                if error_code != None:
                                    logger.log_skip(product_directory, error_code)
                        else:
                            logger.log_skip(product_directory, error_code)
                    else:
                        error_code = "PROD_UNTERSCHIEDLICH"
                        logger.log_skip(product_directory, error_code)
            logger.print_manufacturer_summary()

logger.print_end_time()

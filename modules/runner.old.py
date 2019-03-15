import os
import json

from modules.archiver import archive_exports
from modules.validator import validate_fields, validate_setup
from modules.parser.prod import parse_product
from modules.parser.ilugg import parse_manufacturer_information

from modules.logger import Logger

logger = Logger()

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

def get_manufacturer_information(manufacturer_path, manufacturer_name):
    ilugg_path = manufacturer_path + "/" + manufacturer_name + MANUFACTURER_INFO_ENDING
    if not os.path.exists(ilugg_path):
        logger.set_manufacturer(manufacturer_name)
        logger.log_skip("ILUGG", "NICHT_VORHANDEN")
        logger.unset_manufacturer()
        return None
    manufacturer_information = parse_manufacturer_information(ilugg_path)
    if not manufacturer_information:
        logger.set_manufacturer(manufacturer_name)
        logger.log_skip("ILUGG", "NICHT_AUSWERTBAR")
        logger.unset_manufacturer()
        return None
    return manufacturer_information


def run(do_configurator_export, do_complete_export, do_price_export, do_shop_export, limited_manufacturers):
    if os.path.exists(RUNNING_INDICATOR):
        print("Es läuft bereits ein Export!")
        return

    running_indicator = open(RUNNING_INDICATOR, "w")
    running_indicator.close()

    try:
        logger.print_start_time()
        archive_exports(GENERAL_CONFIG_FILE)

        if do_configurator_export:
            configurator_exporter = ConfiguratorExporter(GENERAL_CONFIG_FILE, CONFIGURATOR_NAME)
        if do_complete_export:
            complete_exporter = CompleteExporter(GENERAL_CONFIG_FILE, COMPLETE_NAME, manufacturers)
        if do_price_export:
            price_exporter = PriceExporter(GENERAL_CONFIG_FILE, PRICE_NAME, PRICE_CONFIG)
        if do_shop_export:
            shop_exporter = ShopExporter(GENERAL_CONFIG_FILE, SHOP_NAME, MANUFACTURER_ENDING)


        for manufacturer_name, manufacturer in manufacturers.items():
            manufacturer_path = manufacturer["path"]
            logger.set_manufacturer(manufacturer_name)

            # Die Hersteller Informationen werden nur für den Shop-Export benötigt
            if do_shop_export:
                manufacturer_information = get_manufacturer_information(
                    manufacturer_path,
                    manufacturer_name
                )

            if not do_configurator_export and limited_manufacturers and not manufacturer_name in limited_manufacturers:
                continue

            for product_name, product_path in manufacturer["products"].items():
                logger.print_manufacturer_progress()
                if not os.path.exists(product_path):
                    logger.log_skip(product_name, "PROD_UNTERSCHIEDLICH")
                    continue

                fields, attribute_names, attribute_types = parse_product(product_path)
                error_code = validate_fields(fields, PRODUCT_TYPE_ID)
                if error_code != None:
                    logger.log_skip(product_name, error_code)
                    continue

                if do_configurator_export:
                    flattened_fields = flatten_fields(fields)
                    product_type = flattened_fields[PRODUCT_TYPE_ID]
                    configurator_exporter.write_to_csv(flattened_fields, product_type)

                if do_complete_export:
                    complete_exporter.write_to_csv(manufacturer_name, fields)

                if do_price_export:
                    price_exporter.write_to_csv(manufacturer_name, fields)

                if do_shop_export:
                    if manufacturer_information == None:
                        continue

                    if not limited_manufacturers or manufacturer_name in limited_manufacturers:
                        error_code = shop_exporter.write_to_csv(
                            fields,
                            attribute_names,
                            attribute_types,
                            manufacturer_information,
                            manufacturer_name
                        )

            logger.print_manufacturer_summary()

        logger.print_end_time()
        print("")
    except Exception as exception:
        raise
    finally:
        os.remove(RUNNING_INDICATOR)

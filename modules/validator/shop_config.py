import os
import sys
import json
from .helpers import validate_required_fields

shop_config_value_types = [ "iterierbar", "wert", "prod", "ilugg" ]
iterable_max_value_types = shop_config_value_types[1:]
shop_iterable_value_fields = [ "praefix", "max" ]

def validate_shop_config(export_configs_directory, shop_name):
    shop_config_path = export_configs_directory + shop_name + ".json"
    if not os.path.exists(shop_config_path):
        sys.exit(
            "[FEHLER] Es gibt keine '{}.json' Datei in {}"
            .format(shop_name, export_configs_directory)
        )

    with open(shop_config_path, "r", encoding="utf-8") as shop_config_file:
        shop_config = json.load(shop_config_file)

    for name, specification in shop_config.items():
        if len(list(specification.keys())) != 1:
            sys.exit(
                "[FEHLER] Zu viele Werte in {} für '{}'"
                .format(shop_config_path, name)
            )
        key = list(specification.keys())[0]
        if not key in shop_config_value_types:
            sys.exit(
                "[FEHLER] Unbekannter Bezeichner '{}' für Wert von '{}' in {}"
                .format(key, name, shop_config_path)
            )
        if key == "iterierbar":
            validate_required_fields(
                specification["iterierbar"],
                shop_config_path,
                shop_iterable_value_fields,
                "Der iterierbare Wert '{}' in ".format(name)
            )

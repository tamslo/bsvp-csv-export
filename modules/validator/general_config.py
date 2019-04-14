import os
import sys
import json
from .helpers import validate_required_fields, validate_list

general_config_fields = [
    "konfigurator-csv-separator",
    "shop-csv-separator",
    "csv-encoding"
]

def validate_general_config(general_config_file, configurator_name, shop_name):
    # Überprüfung, ob es die config.json Datei gibt
    if not os.path.exists(general_config_file):
        sys.exit(
            "[FEHLER] Die generelle Konfiguration {} fehlt"
            .format(general_config_file)
        )

    # Konfiguration aus config.json auslesen
    with open(general_config_file, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    # Überprüfung, ob es die erforderlichen Felder gibt
    validate_required_fields(config, general_config_file, general_config_fields)

    # Validierung des angegebenen Encodings
    test_path = "test.csv"
    try:
        test_file = open(test_path, "w", encoding=config["csv-encoding"])
        test_file.close()
        os.remove(test_path)
    except:
        os.remove(test_path)
        sys.exit(
            "[FEHLER] Die Export-Konfiguration in {} enthält invalides Encoding {}"
            .format(export_config_path, encoding)
        )
    return config

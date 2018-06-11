# -*- coding: utf-8 -*-
import sys, os, json
from modules.configurator.formatter import format_rules

# Erforderliche Felder

general_config_fields = [
    "konfigurator-csv-separator",
    "shop-csv-separator",
    "csv-encoding",
    "configs-ordner",
    "bsvp-ordner",
    "export-ordner"
]

general_config_directories = [
    "configs-ordner",
    "bsvp-ordner",
    "export-ordner"
]

shop_config_value_types = [ "iterierbar", "wert", "prod", "ilugg" ]
iterable_max_value_types = shop_config_value_types[1:]
shop_iterable_value_fields = [ "praefix", "max" ]

# Hilfsmethoden

def validate_required_fields(config, file_path, required_fields, prefix = ""):
    for required_field in required_fields:
        if not required_field in config:
            sys.exit(
                "[FEHLER] {}{} enthält kein Feld '{}'"
                .format(prefix, file_path, required_field)
            )

def validate_list(config, field, file_path, insertion = ""):
    if not isinstance(config[field], list):
        sys.exit(
            "[FEHLER] Das Feld '{}' {}in {} enthält keine Liste"
            .format(field, insertion, file_path)
        )

# Teile von der Setup-Validierung

def validate_export_config(config, export_config_path):
    required_fields = ["produkttyp" ,"felder"]
    validate_required_fields(config, export_config_path, required_fields)
    if "hersteller_export" in config:
        validate_list(config, "hersteller_export", export_config_path)
    validate_combinations(config, export_config_path)
    validate_formatters(config, export_config_path)

def validate_combinations(config, export_config_path):
    if "kombinationen" in config:
        for name, combination in config["kombinationen"].items():
            required_fields = ["separator", "felder"]
            validate_required_fields(
                combination,
                export_config_path,
                required_fields,
                "Kombination {} in ".format(name)
            )
            validate_list(
                combination,
                "felder",
                export_config_path,
                "in Kombination {} ".format(name)
            )

def validate_formatters(config, export_config_path):
    if "formatierungen" in config:
        rules = format_rules()
        for format_rule in config["formatierungen"]:
            if not format_rule in rules:
                sys.exit(
                    "[FEHLER] Ungültige Formatierungsregel {} in {}"
                    .format(format_rule, export_config_path)
                )
            validate_list(
                config["formatierungen"],
                format_rule,
                export_config_path,
                "in 'formatierungen' "
            )

        if "ersetzungen" in config["formatierungen"]:
            for index, replacement in enumerate(config["formatierungen"]["ersetzungen"]):
                required_fields = ["vorher", "nachher", "felder"]
                validate_required_fields(
                    replacement,
                    export_config_path,
                    required_fields,
                    "Die {}. Ersetzung in 'formatierungen' ".format(index + 1)
                )

                validate_list(
                    replacement,
                    "vorher",
                    export_config_path,
                    "in der {}. Ersetzung in 'formatierungen' ".format(index + 1)
                )

                validate_list(
                    replacement,
                    "felder",
                    export_config_path,
                    "in der {}. Ersetzung in 'formatierungen' ".format(index + 1)
                )

# Tatsächlich genutzte Funktionen

def validate_setup(general_config_file, configurator_name, shop_name):
    if not os.path.exists(general_config_file):
        sys.exit(
            "[FEHLER] Die generelle Konfiguration fehlt, es gibt keine Datei {}"
            .format(general_config_file)
        )

    config_file = open(general_config_file, "r", encoding="utf-8")
    config = json.load(config_file)
    export_configs_directory = config["configs-ordner"]
    if not os.path.isdir(export_configs_directory):
        sys.exit(
            "[FEHLER] Die Export-Konfigurationen fehlen, es gibt keinen Ordner {}"
            .format(export_configs_directory)
        )

    configurator_configs_directory = export_configs_directory + configurator_name + "/"
    if not os.path.isdir(configurator_configs_directory):
        sys.exit(
            "[FEHLER] Es gibt keinen Ordner '{}' in {}"
            .format(configurator_name, export_configs_directory)
        )

    shop_config_path = export_configs_directory + shop_name + ".json"
    if not os.path.exists(shop_config_path):
        sys.exit(
            "[FEHLER] Es gibt keine '{}.json' Datei in {}"
            .format(shop_name, export_configs_directory)
        )

    validate_required_fields(config, export_configs_directory, general_config_fields)
    for directory_field in general_config_directories:
        if not config[directory_field].endswith("/"):
            sys.exit(
                "[FEHLER] Das Verzeichnis {} in {} muss mit '/' enden"
                .format(directory_field, general_config_file)
            )

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

    for export_config in os.listdir(configurator_configs_directory):
        export_config_path = configurator_configs_directory + export_config
        with open(export_config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            validate_export_config(config, export_config_path)

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


    config_file.close()

def validate_fields(fields, product_type_id):
    if not "ARTNR" in fields:
        return "KEINE_ARTNR"
    if not "DELSTAT" in fields:
        return "KEIN_DELSTAT"
    if not "TECHDATA" in fields:
        return "KEIN_TECHDATA"
    if not fields["TECHDATA"]:
        return "TECHDATA_LEER"
    if not product_type_id in fields["TECHDATA"]:
        return "KEIN_PRODUKTTYP"
    return None

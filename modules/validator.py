# -*- coding: utf-8 -*-
import sys, os, json

def validate_fields(fields, product_type_id):
    if not "ARTNR" in fields:
        return "KEINE_ARTNR"
    if not "TECHDATA" in fields:
        return "KEIN_TECHDATA"
    if not fields["TECHDATA"]:
        return "TECHDATA_LEER"
    if not product_type_id in fields["TECHDATA"]:
        return "KEIN_PRODUKTTYP"
    return None

def validate_required_fields(config, required_fields):
    for required_field in required_fields:
        if not required_field in config:
            sys.exit(
                "[FEHLER] {} enthält kein Feld {}"
                .format(file_path, required_field)
            )

def validate_setup(general_config_file):
    if not os.path.exists(general_config_file):
        sys.exit(
            "[FEHLER] Die generelle Konfiguration fehlt, es gibt keine Datei {}"
            .format(general_config_file)
        )

    config_file = open(general_config_file, "r", encoding="utf-8")
    config = json.load(config_file)
    export_configs_directory = config["configs_directory"]

    required_fields = [
        "separator",
        "encoding",
        "bsvp_data_directory",
        "output_directory",
        "archive_directory"
    ]
    directory_fields = [
        "bsvp_data_directory",
        "output_directory",
        "archive_directory"
    ]


    if not os.path.exists(export_configs_directory):
        sys.exit(
            "[FEHLER] Die Export-Konfigurationen fehlen, es gibt keinen Ordner {}"
            .format(export_configs_directory)
        )

    validate_required_fields(config, required_fields)
    for directory_field in directory_fields:
        if not config[directory_field].endswith("/"):
            sys.exit(
                "[FEHLER] Das Verzeichnis {} in {} muss mit '/' enden"
                .format(directory_field, general_config_file)
            )

    # Validierung des angegebenen Encodings
    test_path = "test.csv"
    try:
        test_file = open(test_path, "w", encoding=config["encoding"])
        test_file.close()
        os.remove(test_path)
    except:
        os.remove(test_path)
        sys.exit(
            "[FEHLER] Die Export-Konfiguration in {} enthält invalides Encoding {}"
            .format(export_config_path, encoding)
        )

    for export_config in os.listdir(export_configs_directory):
        required_fields = ["produkttyp" ,"felder"]
        export_config_path = export_configs_directory + export_config
        with open(export_config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            validate_required_fields(config, required_fields)
            if not "ARTNR" in config["felder"]:
                sys.exit("[FEHLER] {} enthält keine ARTNR").format(export_config_path)
            if not "TECHDATA" in config["felder"]:
                sys.exit("[FEHLER] {} enthält keine TECHDATA").format(export_config_path)
            if "kombinationen" in config:
                for name, combination in config["kombinationen"].items():
                    if not "separator" in combination:
                        sys.exit(
                            "[FEHLER] Kombination {} in {} enthält kein Feld separator"
                            .format(name, export_config_path)
                        )
                    if not "feld" in combination:
                        sys.exit(
                            "[FEHLER] Kombination {} in {} enthält kein Feld feld"
                            .format(name, export_config_path)
                        )
                    if not "felder" in combination:
                        sys.exit(
                            "[FEHLER] Kombination {} in {} enthält kein Feld felder"
                            .format(name, export_config_path)
                        )
                    if not isinstance(combination["felder"], list):
                        sys.exit(
                            "[FEHLER] Das Feld felder in Kombination {} in {} enthält keine Liste"
                            .format(name, export_config_path)
                        )

    config_file.close()

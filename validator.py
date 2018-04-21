# -*- coding: utf-8 -*-
import sys, os, json

def validate_config(file_path, required_fields):
    with open(file_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        for required_field in required_fields:
            if not required_field in config:
                sys.exit(
                    "[FEHLER] {} enthält kein Feld {}"
                    .format(file_path, required_field)
                )

def validate_directories(file_path, directory_fields):
    with open(file_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        for directory_field in directory_fields:
            if not config[directory_field].endswith("/"):
                sys.exit(
                    "[FEHLER] Das Verzeichnis {} in {} muss mit '/' enden"
                    .format(directory_field, file_path)
                )

def validate_setup(general_config_file, export_configs_directory):
    if not os.path.exists(general_config_file):
        sys.exit(
            "[FEHLER] Die generelle Konfiguration fehlt, es gibt keine Datei {}"
            .format(general_config_file)
        )

    if not os.path.exists(export_configs_directory):
        sys.exit(
            "[FEHLER] Die Export-Konfigurationen fehlen, es gibt keinen Ordner {}"
            .format(export_configs_directory)
        )

    required_fields = [
        "separator",
        "encoding",
        "bsvp_data_directory",
        "output_directory",
        "archive_directory"
    ]
    validate_config(general_config_file, required_fields)
    validate_directories(general_config_file, [
        "bsvp_data_directory",
        "output_directory",
        "archive_directory"
    ])

    # Validierung des angegebenen Encodings
    with open(general_config_file, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
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
        required_fields = ["produkttyp" ,"attribute"]
        validate_config(
            export_configs_directory + export_config,
            required_fields
        )

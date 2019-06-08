import os, json
from collections import OrderedDict

def transform_configs(configs_directory, output_directory):
    # Schreibe Konfigurationen so um, dass sie über den Produkttyp als Key
    # erreichbar sind.
    configs = OrderedDict()

    for export_config_name in os.listdir(configs_directory):
        if export_config_name.endswith(".json"):
            export_config_path = configs_directory + export_config_name
            with open(export_config_path, "r",  encoding="utf-8") as export_config_file:
                export_config = json.load(export_config_file, object_pairs_hook=OrderedDict)

            config_name = output_directory + export_config_name.split(".json")[0]
            base_output_path = config_name + ".csv"

            # Schreibe einen Output für die allgemeine Konfigurator CSV-Datei für
            # den aktuellen Produkttyp und einen pro definiertem Hersteller
            export_config["outputs"] = [{ "base": True, "path": base_output_path }]
            if "hersteller_export" in export_config:
                for manufacturer in export_config["hersteller_export"]:
                    manufacturer_output_path = "{}_{}.csv".format(
                        config_name,
                        manufacturer
                    )
                    export_config["outputs"].append({
                        "base": False,
                        "manufacturer": manufacturer,
                        "path": manufacturer_output_path
                    })

            # Im Exporter werden Kombinationen und Formatierungen nicht noch
            # einmal geprüft, wenn es keine gibt, wird einfach ein leeres
            # Objekt eingesetzt, über das dann iteriert werden kann.
            if not "kombinationen" in export_config:
                export_config["kombinationen"] = {}
            if not "formatierungen" in export_config:
                export_config["formatierungen"] = {}

            # Vorhandene Formatierungen in das vom Formatter benötigte Format
            # bringen, in dem für jedes Feld Formatierungsoptionen aufgelistet
            # werden.

            def add_format_option(format_options, field, option):
                if field in format_options:
                    format_options[field].append(option)
                else:
                    format_options[field] = [option]

            if "formatierungen" in export_config:
                format_options = {}
                for option in export_config["formatierungen"]:
                    if option == "ersetzungen":
                        for ersetzung in export_config["formatierungen"][option]:
                            for field in ersetzung["felder"]:
                                option = {
                                    "type": "ersetzung",
                                    "before": ersetzung["vorher"],
                                    "afterwards": ersetzung["nachher"]
                                }
                                add_format_option(format_options, field, option)
                    else:
                        for field in export_config["formatierungen"][option]:
                            option = { "type": option }
                            add_format_option(format_options, field, option)
                export_config["formatierungen"] = format_options

            product_type = export_config["produkttyp"]
            configs[product_type] = export_config

    return configs

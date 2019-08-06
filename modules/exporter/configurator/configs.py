import os, json
from collections import OrderedDict

def sort_format_options(export_config, format_options):
    for ordering in export_config["reihenfolgen"]:
        formatter_ordering = ordering["reihenfolge"]
        for field in ordering["felder"]:
            if field in format_options:
                field_options = format_options[field]
                ordered_field_options = []
                covered_indices = []
                for formatter_position in formatter_ordering:
                    field_option_index = next((index
                        for (index, field_option) in enumerate(field_options)
                        if "id" in field_option and field_option["id"] == formatter_position), None)
                    if field_option_index != None:
                        field_option = field_options[field_option_index]
                        ordered_field_options.append(field_option)
                        covered_indices.append(field_option_index)
                for index, field_option in enumerate(field_options):
                    if not index in covered_indices:
                        ordered_field_options.append(field_option)
                format_options[field] = ordered_field_options
    return format_options


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

            def build_format_option(option, parameters=None):
                format_option = { "type": option }
                if parameters != None and "id" in parameters:
                    format_option["id"] = parameters["id"]
                return format_option

            def add_format_option(format_options, field, option):
                if field in format_options:
                    format_options[field].append(option)
                else:
                    format_options[field] = [option]

            # Formatierungen so umschreiben, dass sie durch die Feld ID erreichbar sind.
            # Für jedes Feld wird eine Liste von Formatierungen angegeben.
            # Wenn Reihenfolgen angegeben sind, werden diese Listen so sortiert, dass
            # zuerst die Formatierungen mit spezifizierter Reihenfolge bearbeitet werden.
            if "formatierungen" in export_config:
                format_options = {}
                for option in export_config["formatierungen"]:
                    if option == "ersetzungen" or option == "gruppierungen":
                        for parameters in export_config["formatierungen"][option]:
                            for field in parameters["felder"]:
                                format_option = build_format_option(option, parameters)
                                if option == "ersetzungen":
                                    format_option["before"] = parameters["vorher"]
                                    format_option["afterwards"] = parameters["nachher"]
                                    format_option["option"] = "option" in parameters and parameters["option"] or None
                                else: # option == "gruppierungen":
                                    format_option["thresholds"] = parameters["grenzwerte"]
                                    format_option["unit"] = parameters["einheit"]
                                add_format_option(format_options, field, format_option)
                    else:
                        for field in export_config["formatierungen"][option]:
                            format_option = build_format_option(option)
                            add_format_option(format_options, field, format_option)
                # Formatierungen pro Feld ggf. sortieren
                if "reihenfolgen" in export_config:
                    format_options = sort_format_options(export_config, format_options)
                export_config["formatierungen"] = format_options

            product_type = export_config["produkttyp"]
            configs[product_type] = export_config

    return configs

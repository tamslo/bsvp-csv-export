import os
import sys
import json
from modules.exporter.configurator.formatter import format_rules
from .helpers import validate_required_fields, validate_list

export_config_fields = ["produkttyp" ,"felder"]
combination_fields = ["separator", "felder"]
combination_lists = ["felder"]
replacement_fields = ["vorher", "nachher", "felder"]
replacement_lists = ["vorher", "felder"]

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
                validate_required_fields(
                    replacement,
                    export_config_path,
                    replacement_fields,
                    "Die {}. Ersetzung in 'formatierungen' ".format(index + 1)
                )
                for field in replacement_lists:
                    validate_list(
                        replacement,
                        field,
                        export_config_path,
                        "in der {}. Ersetzung in 'formatierungen' ".format(index + 1)
                    )

def validate_combinations(config, export_config_path):
    if "kombinationen" in config:
        for name, combination in config["kombinationen"].items():
            validate_required_fields(
                combination,
                export_config_path,
                combination_fields,
                "Kombination {} in ".format(name)
            )
            for field in combination_lists:
                validate_list(
                    combination,
                    field,
                    export_config_path,
                    "in Kombination {} ".format(name)
                )

def validate_export_config(config, export_config_path):
    validate_required_fields(config, export_config_path, export_config_fields)
    if "hersteller_export" in config:
        validate_list(config, "hersteller_export", export_config_path)
    validate_combinations(config, export_config_path)
    validate_formatters(config, export_config_path)

def validate_configurator_configs(export_configs_directory, configurator_name):
    configurator_configs_directory = export_configs_directory + configurator_name + "/"
    if not os.path.isdir(configurator_configs_directory):
        sys.exit(
            "[FEHLER] Es gibt keinen Ordner '{}' in {}"
            .format(configurator_name, export_configs_directory)
        )

    for export_config in os.listdir(configurator_configs_directory):
        export_config_path = configurator_configs_directory + export_config
        with open(export_config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            validate_export_config(config, export_config_path)

import os, sys
import yaml
from modules import formatter
from modules.formatter import formatters
from .helpers import validate_required_fields, validate_list

replacement_fields = ["vorher", "nachher", "felder"]
replacement_lists = ["vorher", "felder"]

def validate_format_config(export_configs_directory, format_config_file_name):
    if format_config_file_name in os.listdir(export_configs_directory):
        format_config_file_path = os.path.join(export_configs_directory, format_config_file_name)
        with open(os.path.join(format_config_file_path), "r") as formatting_config_file:
            format_config = yaml.load(formatting_config_file, Loader=yaml.FullLoader)

        for format_rule in format_config:
            validate_list(
                format_config,
                format_rule,
                format_config_file_path,
                "in 'formatierungen' "
            )

        if "ersetzungen" in format_config:
            for index, replacement in enumerate(format_config["ersetzungen"]):
                validate_required_fields(
                    replacement,
                    format_config_file_path,
                    replacement_fields,
                    "Die {}. Ersetzung in 'formatierungen' ".format(index + 1)
                )
                for field in replacement_lists:
                    validate_list(
                        replacement,
                        field,
                        format_config_file_path,
                        "in der {}. Ersetzung in 'formatierungen' ".format(index + 1)
                    )
                if "option" in replacement:
                    allowed_options = ["startswith", "endswith"]
                    option = replacement["option"]
                    if not option in allowed_options:
                        sys.exit(
                            "[FEHLER] Ungültige Option '{}' in der {}. Ersetzung in 'formatierungen' der {}"
                            .format(option, index + 1, format_config_file_path)
                        )
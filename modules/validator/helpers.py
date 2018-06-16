import sys

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

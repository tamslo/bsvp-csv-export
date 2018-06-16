from .general_config import validate_general_config
from .shop_config import validate_shop_config
from .configurator_configs import validate_configurator_configs

def validate_setup(general_config_file, configurator_name, shop_name):
    export_configs_directory, config = validate_general_config(
        general_config_file,
        configurator_name,
        shop_name
    )
    validate_configurator_configs(export_configs_directory, configurator_name)
    validate_shop_config(export_configs_directory, shop_name)


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

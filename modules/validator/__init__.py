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

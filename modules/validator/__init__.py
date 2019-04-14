from .general_config import validate_general_config
from .shop_config import validate_shop_config
from .configurator_configs import validate_configurator_configs
from modules.constants import CONFIGS_DIRECTORY

def validate_setup(general_config_file, configurator_name, shop_name):
    config = validate_general_config(
        general_config_file,
        configurator_name,
        shop_name
    )
    validate_configurator_configs(CONFIGS_DIRECTORY, configurator_name)
    validate_shop_config(CONFIGS_DIRECTORY, shop_name)

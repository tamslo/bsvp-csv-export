import argparse
from modules.runner import run

# Kommandozeilen-Argumente definieren und auslesen

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--configurator",
    help="nur den Konfigurator Export starten",
    action="store_true"
)
parser.add_argument(
    "-s", "--shop",
    help="nur den Shop Export starten - wenn Hersteller Ordner angegeben werden, werden nur diese exportiert",
    nargs="*",
    metavar="hersteller",
    default=None
)

args = parser.parse_args()
do_configurator_export = args.configurator
do_shop_export = args.shop != None
# Wenn Hersteller-Ordner angegeben sind, ist limited_manufacturers eine Liste,
# sonst False
limited_manufacturers = isinstance(args.shop, list) and len(args.shop) > 0 and args.shop

run(do_configurator_export, do_shop_export, limited_manufacturers)

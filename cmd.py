import argparse
from modules.runner import run

# Kommandozeilen-Argumente definieren und auslesen

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--configurator",
    help="den Konfigurator Export starten",
    action="store_true"
)
parser.add_argument(
    "-a", "--all",
    help="den kompletten Export starten",
    action="store_true"
)
parser.add_argument(
    "-p", "--preis",
    help="Listenpreise pro Hersteller exportieren",
    action="store_true"
)
parser.add_argument(
    "-s", "--shop",
    help="den Shop Export starten - wenn Hersteller Ordner angegeben werden, werden nur diese exportiert",
    nargs="*",
    metavar="hersteller",
    default=None
)

args = parser.parse_args()
do_configurator_export = args.configurator
do_complete_export = args.all
do_price_export = args.preis
do_shop_export = args.shop != None
# Wenn Hersteller-Ordner angegeben sind, ist limited_manufacturers eine Liste,
# sonst False
limited_manufacturers = isinstance(args.shop, list) and len(args.shop) > 0 and args.shop

# Wenn kein Parameter angegeben ist, dann wird alles exportiert
if not do_configurator_export and not do_complete_export and not do_shop_export and not do_price_export:
    do_configurator_export = True
    do_complete_export = True
    do_shop_export = True
    do_price_export = True

run(do_configurator_export, do_complete_export, do_price_export, do_shop_export, limited_manufacturers)

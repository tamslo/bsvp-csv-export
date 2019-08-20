from modules.logger import Logger
from ..utils.include_tooltips import include_tooltips

max_placeholders = 5
def placeholder(index):
    return "$BT_Passage{}$".format(index)

def replacement(ilugg_fields, index):
    return ilugg_fields["P{}Value".format(index)]

def export_general_description(parameters):
    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]
    tooltips = parameters["tooltips"]

    welcome_text = ""
    if "WELCOMETEXT" in prod_fields and prod_fields["WELCOMETEXT"] != "":
        welcome_text = prod_fields["WELCOMETEXT"]
    elif ("WELCOMETHISTEXT" in prod_fields):
        welcome_text = prod_fields["WELCOMETHISTEXT"]
    else:
        Logger().log("[WARNUNG] {} hat kein WELCOMETEXT und kein WELCOMETHISTEXT Feld".format(
            prod_fields["ARTNR"]
        ))

    index = 1
    while index <= max_placeholders:
        welcome_text = welcome_text.replace(
            placeholder(index),
            replacement(ilugg_fields, index)
        )
        index += 1

    text = welcome_text + prod_fields["DESC"]
    return include_tooltips(tooltips, text)

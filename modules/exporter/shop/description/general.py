from modules.logger import Logger

max_placeholders = 5
def placeholder(index):
    return "$BT_Passage{}$".format(index)

def replacement(ilugg_fields, index):
    return ilugg_fields["P{}Value".format(index)]

def export_general_description(prod_fields, ilugg_fields):
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

    return welcome_text + prod_fields["DESC"]

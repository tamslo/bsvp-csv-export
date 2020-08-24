from modules.logger import Logger

def placeholder(index):
    return "$BT_Passage{}$".format(index)

def replacement(ilugg_fields, index):
    return ilugg_fields["P{}Value".format(index)]

def get_welcome_text(prod_fields, ilugg_fields):
    max_placeholders = 5
    welcome_text = ""

    if not "ARTWELCOMESTATE" in prod_fields:
        Logger().log("[WARNUNG] {} hat kein ARTWELCOMESTATE Feld".format(
            prod_fields["ARTNR"]
        ))
        return welcome_text
    welcome_state = prod_fields["ARTWELCOMESTATE"]

    if welcome_state == "0":
        if not "WELCOMETHISTEXT" in prod_fields:
            Logger().log("[WARNUNG] {} mit ARTWELCOMESTATE 0 hat kein WELCOMETHISTEXT Feld".format(
                prod_fields["ARTNR"]
            ))
            return welcome_text
        welcome_text = prod_fields["WELCOMETHISTEXT"]

    if welcome_state == "1":
        index = 1
        while index <= max_placeholders:
            welcome_text = welcome_text + placeholder(index)
            index += 1

    if welcome_state == "2":
        if not "WELCOMETEXT" in prod_fields:
            Logger().log("[WARNUNG] {} mit ARTWELCOMESTATE 2 hat kein WELCOMETEXT Feld".format(
                prod_fields["ARTNR"]
            ))
            return welcome_text
        welcome_text = prod_fields["WELCOMETEXT"]

    index = 1
    while index <= max_placeholders:
        welcome_text = welcome_text.replace(
            placeholder(index),
            replacement(ilugg_fields, index)
        )
        index += 1

    return welcome_text

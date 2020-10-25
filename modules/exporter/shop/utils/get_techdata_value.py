from modules.logger import Logger

def get_value(fields, field_id, warn=False, prod_fields=None):
    prod_fields = prod_fields or fields
    if field_id in fields:
        return fields[field_id]
    else:
        if warn:
            warning_text = prod_fields["ARTNR"]
            warning_text += ": Kein Wert für das Feld '"
            warning_text += field_id
            warning_text += "'. Das Feld in der Tabelle bleibt leer."
            Logger().log(warning_text)
        return ""

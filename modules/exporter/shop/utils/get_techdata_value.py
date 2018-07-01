def get_value(fields, field_id, warn=False):
    if field_id in fields:
        return fields[field_id]
    else:
        if warn:
            warning_text = "[ACHTUNG] Kein Wert für das Feld '"
            warning_text += field_id
            warning_text += "' im Produkt mit der Artikelnummer"
            warning_text += prod_fields["ARTNR"]
            warning_text += " von " + prod_fields["MANUFACTURER"]
            warning_text += ". Das Feld in der Tabelle bleibt leer."
            print(warning_text)
        return ""
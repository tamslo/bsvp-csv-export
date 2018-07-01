from .table import Table

def get_value(fields, field_id):
    if field_id in fields:
        return fields[field_id]
    else:
        return ""

def should_build_table(prod_fields):
    if "ENERGYCLASS" in prod_fields:
        return prod_fields["ENERGYCLASS"] != ""

def export_energy_efficiency_text(parameters):
    prod_fields = parameters["prod_fields"]
    attribute_names = parameters["attribute_names"]
    tooltips = parameters["tooltips"]
    rows = parameters["specification"]["fields"]
    techdata = prod_fields["TECHDATA"]
    table = Table(tooltips)

    if should_build_table(prod_fields):
        table.make_header("Anschluss- und Verbrauchswerte")
        for field_id in rows:
            field_name = get_value(attribute_names, field_id)
            if (field_name == ""):
                warning_text = "[ACHTUNG] Kein Attributname im "
                warning_text += "energy_efficiency_text für das Feld '"
                warning_text += field_id
                warning_text += "' im Produkt mit der Artikelnummer"
                warning_text += prod_fields["ARTNR"]
                warning_text += " von " + prod_fields["MANUFACTURER"]
                warning_text += ". Das Feld in der Tabelle bleibt leer."
                print(warning_text)
            table.make_row(
                field_name,
                get_value(techdata, field_id)
            )
        return table.to_string()

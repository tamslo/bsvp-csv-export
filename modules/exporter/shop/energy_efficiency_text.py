from .table import Table

rows = [
    {
        "description": "Anschlusswert in Watt",
        "field_id": "0000015"
    }, {
        "description": "Energieverbrauch in kWh / 24h",
        "field_id": "0000089"
    },
    {
        "description": "Energieverbrauch 365 Tage",
        "field_id": "0000264"
    },
    {
        "description": "Energieeffizienzklasse",
        "field_id": "0000265"
    },
    {
        "description": "Energieeffizienzindex",
        "field_id": "0000339"
    },
    {
        "description": "Nettorauminhalt Kühlung gesamt",
        "field_id": "0000337"
    },
    {
        "description": "Nettorauminhalt Tiefkühlung gesamt",
        "field_id": "0000338"
    },
    {
        "description": "Kältemittelsorte / GWP",
        "field_id": "0000139"
    },
    {
        "description": "Klimaklasse",
        "field_id": "0000142"
    },
    {
        "description": "Geräuschpegel in dB(A)",
        "field_id": "0000109"
    },
    {
        "description": "Frequenz in Hz",
        "field_id": "0000099"
    },
    {
        "description": "Spannung in Volt",
        "field_id": "0000213"
    }
]

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
    table = Table(tooltips)

    if should_build_table(prod_fields):
        table.make_header("Anschluss- und Verbrauchswerte")
        for row_specification in rows:
            field_id = row_specification["field_id"]
            field_name = get_value(attribute_names, field_id)
            if (get_value(attribute_names, field_id) == ""):
                warning_text = "[ACHTUNG] Kein Attributname im "
                warning_text += "energy_efficiency_text für das Feld '"
                warning_text += field_id
                warning_text += "' im Produkt mit der Artikelnummer"
                warning_text += prod_fields["ARTNR"]
                warning_text += ". Das Feld in der Tabelle bleibt leer."
                print(warning_text)
            table.make_row(
                field_name,
                get_value(prod_fields, field_id)
            )
        return table.to_string()

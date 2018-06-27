from . import table

body_rows = [
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

def get_value(prod_fields, field_id):
    if field_id in prod_fields:
        return prod_fields[field_id]
    else:
        return ""

def export_energy_efficiency_text(prod_fields):
    rows = []
    rows.append(table.header_row("Anschluss- und Verbrauchswerte"))
    for row_specification in body_rows:
        field_id = row_specification["field_id"]
        rows += table.body_row(
            row_specification["description"],
            get_value(prod_fields, field_id)
        )

    if len(rows) > 1:
        return table.table("".join(rows))
    else:
        return None
